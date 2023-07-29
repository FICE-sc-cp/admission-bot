import logging
from datetime import datetime

from aiogram import types
from aiogram.utils import exceptions
from pymongo import ReturnDocument

import config
import db
import keyboards
from main import AdmissionQueue
from stages import Stage
from utils import get_spherical_distance

logger = logging.getLogger('commands')


def apply_handlers(aq: AdmissionQueue):
    async def start_handler(message: types.Message):
        user = await db.users.find_one({'uid': message.chat.id})
        if user is not None:
            if user['stage'] == Stage.menu:
                await message.answer(
                    "<b>Електронна черга ФІОТ</b>\n\nДля реєстрації у черзі на подання документів, натисніть \"Усі черги\" та оберіть необхідну вам.\n\nЯкщо у вас виникнуть якісь запитання чи проблеми, натисніть кнопку \"Допомога\" та напишіть нам про це.\n\nЯкщо ви хочете прискорити подання документів, натисніть кнопку <b>Продовжити реєстрацію</b>.",
                    reply_markup=keyboards.get_menu_kbd(user['lang'],
                                                        user['opt_reg_completed']),
                    parse_mode=types.ParseMode.HTML)
            elif user['stage'] in [Stage.geo, Stage.leave_queue] or (
                    user['stage'] == Stage.template and user['opt_reg']):
                await db.users.find_one_and_update({'uid': user['uid']}, {'$set': {'stage': Stage.menu}})
                await message.answer(
                    "<b>Електронна черга ФІОТ</b>\n\nДля реєстрації у черзі на подання документів, натисніть \"Усі черги\" та оберіть необхідну вам.\n\nЯкщо у вас виникнуть якісь запитання чи проблеми, натисніть кнопку \"Допомога\" та напишіть нам про це.\n\nЯкщо ви хочете прискорити подання документів, натисніть кнопку <b>Продовжити реєстрацію</b>.",
                    reply_markup=keyboards.get_menu_kbd(user['lang'],
                                                        user[
                                                            'opt_reg_completed']),
                    parse_mode=types.ParseMode.HTML)
            elif user['stage'] in [Stage.get_certnum, Stage.get_fio, Stage.template, Stage.register_btns]:
                await db.users.delete_one({'uid': user['uid']})
                await start_handler(message)  # recursive
        else:
            await aq.aapi.register_user(message.from_user.id,
                                        message.from_user.username,
                                        message.from_user.first_name,
                                        message.from_user.last_name)

            now = datetime.now()
            if (now.hour < 10) or (now.hour > 18):
                await message.reply(
                    "Шановні абітурієнти!\nПриймальна комісія працює з 10 до 18. Черги відкриті лише у цей проміжок часу. Зараз ви можете зареєструватись у боті, заповнити свої дані та чекати. Представники приймальної комісії додадуть вас у черги вручну як тільки приїдуть до корпусу, ви будете одними з перших.\nДякуємо за розуміння😊",
                    parse_mode=types.ParseMode.HTML)

            if config.REGISTRATION:
                template = (await aq.aapi.get_registration_template())['template']
                tokens_non_optional = list(filter(lambda x: not x['optional'], template['tokens']))
                num = len(tokens_non_optional)
                user = await db.users.find_one_and_update({'uid': message.chat.id}, {'$set': {'stage': Stage.template,
                                                                                              'template_stage': 0,
                                                                                              'tokens_num': num,
                                                                                              'tokens': tokens_non_optional,
                                                                                              'opt_reg': False,
                                                                                              'opt_reg_completed': False,
                                                                                              'lang': 'ua'}},
                                                          upsert=True, return_document=ReturnDocument.AFTER)
                user['template_stage'] = -1
                await message.reply(
                    "Привіт! Я бот електронної черги на ФІОТ. \nЧерез мене можна зареєструватись у чергу на подання документів 😊",
                    parse_mode=types.ParseMode.HTML)
                await send_token_prompt(user, message)
            else:
                user = db.users.insert_one({'uid': message.chat.id, 'lang': 'ua', 'stage': Stage.menu})
                await message.reply(
                    "<b>Електронна черга ФІОТ</b>\n\nДля реєстрації у черзі на подання документів, натисніть \"Усі черги\" та оберіть необхідну вам.\n\nЯкщо у вас виникнуть якісь запитання чи проблеми, натисніть кнопку \"Допомога\" та напишіть нам про це.\n\nЯкщо ви хочете прискорити подання документів, натисніть кнопку <b>Продовжити реєстрацію</b>.",
                    reply_markup=keyboards.get_menu_kbd(),
                    parse_mode=types.ParseMode.HTML)

    async def help_handler(message: types.Message):
        await message.reply("Задати питання та знайти інформацію можна тут", reply_markup=keyboards.get_info_kbd())

    async def query_handler(query: types.CallbackQuery):
        user = await db.users.find_one({'uid': query.from_user.id})
        if user is None:
            try:
                return await query.answer()
            except exceptions.InvalidQueryID:
                pass  # ignore

        # if query.data.startswith('CertReg'):
        #     await db.users.find_one_and_update({'uid': user['uid']}, {'$set': {'stage': Stage.get_certnum}})
        #     return await query.message.edit_text(t('GET_CERTNUM'))
        #
        # elif query.data.startswith('ManualReg'):
        #     template = (await aq.aapi.get_registration_template())['template']
        #     num = len(template['tokens'])
        #     await db.users.find_one_and_update({'uid': user['uid']}, {'$set': {'stage': Stage.template,
        #                                                                        'template_stage': 0,
        #                                                                        'tokens_num': num,
        #                                                                        'template': template}})
        #     await query.message.answer(template['tokens'][0]['text'])

        elif query.data.startswith('AllQueues'):
            queues = (await aq.aapi.list_queues())['queues']
            num = len(list(filter(lambda x: x['active'], queues)))
            if num > 0:
                await query.message.edit_text("Оберіть чергу, щоб зареєструватись у ній",
                                              reply_markup=keyboards.get_queues_kbd(queues, my_queues=False))
            else:
                try:
                    await query.answer("Наразі немає активних черг")
                except exceptions.InvalidQueryID:
                    pass  # ignore

        elif query.data.startswith('MyQueues'):
            user_data = await aq.aapi.get_user_info(user['uid'])
            queues = user_data['queues']
            num = len(list(filter(lambda x: x['active'], queues)))
            if num > 0:
                await query.message.edit_text("Оберіть чергу, щоб дізнатись свою позицію у ній чи вийти з неї",
                                              reply_markup=keyboards.get_queues_kbd(queues, my_queues=True))
            else:
                try:
                    await query.answer("Ви не зареєстровані у активних чергах")
                except exceptions.InvalidQueryID:
                    pass  # ignore

        elif query.data.startswith('GetQueue'):
            user_data = await aq.aapi.get_user_info(user['uid'])
            queues = user_data['queues']
            queue_id = int(query.data.split('GetQueue', 1)[1])
            if any(map(lambda x: queue_id == x['id'], queues)):  # user already in queue
                query.data = f'GetMyQueue{queue_id}'  # edit data to pass query to GetMyQueue handler
                await query_handler(query)  # recursive call modified query
            else:
                await db.users.find_one_and_update({'uid': user['uid']},
                                                   {'$set': {'get_queue': queue_id, 'stage': Stage.geo}})
                return await query.message.answer(
                    "Надішліть свою геолокацію, щоб підтвердити, що ви знаходитесь на КПІ, та зареєструватись у черзі.",
                    reply_markup=keyboards.get_geo_kbd(user['lang']))

        elif query.data.startswith('GetMyQueue'):
            user_data = await aq.aapi.get_user_info(user['uid'])
            queues = user_data['queues']
            queue_id = int(query.data.split('GetMyQueue', 1)[1])
            try:
                queue = list(filter(lambda x: queue_id == x['id'], queues))[0]
            except IndexError:
                try:
                    return await query.answer("Вас більше немає у цій черзі!")
                except exceptions.InvalidQueryID:
                    return  # ignore
            try:

                if queue['position']['status'] == 'processing':
                    await query.message.edit_text(
                        "<b>{queue_name}</b>\nВаша заявка оброблюється оператором, можете заходити до корпусу.".format(
                            queue_name=queue['name']),
                        reply_markup=keyboards.get_update_my_queue_kbd(queue_id,
                                                                       user['lang']),
                        parse_mode=types.ParseMode.HTML)

                elif queue['position']['status'] == 'waiting':
                    await query.message.edit_text(
                        "<b>{queue_name}</b>\nВаша позиція у черзі: {pos}\nВаш ідентифікаційний номер у черзі: {abs_pos}".format(
                            queue_name=queue['name'],
                            pos=queue['position']['relativePosition'],
                            abs_pos=queue['position']['code']),
                        reply_markup=keyboards.get_update_my_queue_kbd(queue_id,
                                                                       user['lang']),
                        parse_mode=types.ParseMode.HTML)

                else:
                    logger.error('Unknown queue position status', queue['position']['status'])

                await query.answer()
            except exceptions.MessageNotModified:
                try:
                    await query.answer("Немає оновлень")
                except exceptions.InvalidQueryID:
                    pass  # ignore
            except exceptions.InvalidQueryID:
                pass  # ignore

        elif query.data.startswith('LeaveQueue'):
            queue_id = int(query.data.split('LeaveQueue', 1)[1])
            await db.users.find_one_and_update({'uid': user['uid']},
                                               {'$set': {'leave_queue': queue_id, 'stage': Stage.leave_queue}})
            return await query.message.edit_text("Щоб вийти з черги, напишіть у чат \"Так\"", reply_markup=keyboards.get_to_menu_kbd(user['lang']))

        elif query.data.startswith('RegInQueue'):
            queue_id = int(query.data.split('RegInQueue', 1)[1])
            position, code = await aq.aapi.add_user_to_queue(queue_id, user['uid'])
            if code == 400:
                return await query.answer(position['message'])

            if 'position' in position and 'code' in position['position']:
                await query.message.answer_photo(open(f'q_nums/{position["position"]["code"]}.jpg', 'rb'),
                                                 caption="Ваш ідентифікаційний номер у черзі")
            query.data = f'GetMyQueue{queue_id}'  # override query to send current position in queue
            await query_handler(query)

        elif query.data.startswith('Menu'):
            await db.users.find_one_and_update({'uid': user}, {'$set': {'stage': Stage.menu}})
            await query.message.edit_text(
                "<b>Електронна черга ФІОТ</b>\n\nДля реєстрації у черзі на подання документів, натисніть \"Усі черги\" та оберіть необхідну вам.\n\nЯкщо у вас виникнуть якісь запитання чи проблеми, натисніть кнопку \"Допомога\" та напишіть нам про це.\n\nЯкщо ви хочете прискорити подання документів, натисніть кнопку <b>Продовжити реєстрацію</b>.",
                reply_markup=keyboards.get_menu_kbd(user['lang'], user['opt_reg_completed']),
                parse_mode=types.ParseMode.HTML)

        elif query.data.startswith('ChangeData'):
            await db.users.delete_one({'uid': user['uid']})

            query.message.from_user.id = query.from_user.id
            query.message.from_user.username = query.from_user.username
            query.message.from_user.first_name = query.from_user.first_name
            query.message.from_user.last_name = query.from_user.last_name
            await start_handler(query.message)
            await query.message.delete_reply_markup()

        elif query.data.startswith('OptReg'):
            template = (await aq.aapi.get_registration_template())['template']
            tokens_optional = list(filter(lambda x: x['optional'], template['tokens']))
            num = len(tokens_optional)
            user = await db.users.find_one_and_update({'uid': user['uid']}, {'$set': {'stage': Stage.template,
                                                                                      'template_stage': 0,
                                                                                      'tokens_num': num,
                                                                                      'tokens': tokens_optional,
                                                                                      'opt_reg': True,
                                                                                      'opt_reg_completed': False}},
                                                      return_document=ReturnDocument.AFTER)
            user['template_stage'] = -1
            await send_token_prompt(user, query.message)

        elif query.data.startswith('Token'):
            data = {('o_' if user['opt_reg'] else 't_') + user['tokens'][user['template_stage']][
                'token']: query.data.split('Token', 1)[1].strip()}
            await query.message.delete_reply_markup()
            if user['template_stage'] + 1 == user['tokens_num']:
                return await complete_token_registration(user, query.message)

            await send_token_prompt(user, query.message)

            await db.users.find_one_and_update({'uid': user['uid']},
                                               {'$set': {**data},
                                                '$inc': {'template_stage': 1}})

        else:
            logger.warning(f'Got invalid command {query.data}')

        try:
            await query.answer()  # try to answer query if not answered already
        except exceptions.InvalidQueryID:  # already answered
            pass

    async def location_handler(message: types.Message):
        lat = message.location.latitude
        lon = message.location.longitude
        user = await db.users.find_one({'uid': message.from_user.id})

        if user is None:
            return await start_handler(message)

        if user['stage'] != Stage.geo:
            return  # ignore

        if (get_spherical_distance(lat, lon, config.LAT, config.LON) > config.RADIUS) or \
                (message.forward_from is not None):
            return await message.reply(
                "Помилка! Ви ще не знаходитесь на території КПІ, надішліть геолокацію ще раз, коли будете на місці, чи натисніть \"/start\" щоб повернутись у меню\".",
                reply_markup=keyboards.get_geo_kbd())
        else:
            await db.users.find_one_and_update({'uid': message.from_user.id}, {'$set': {'stage': Stage.menu}})
            await message.reply("Ви знаходитесь на КПІ!",
                                reply_markup=types.ReplyKeyboardRemove())

            await message.reply("Ви дійсно хочете зареєструватись у цій черзі?",
                                reply_markup=keyboards.get_register_in_queue_kbd(user['get_queue'], user['lang']))

    async def complete_token_registration(user, message):
        if user['opt_reg']:
            prefix = 'o_'
        else:
            prefix = 't_'
        user[prefix + user['tokens'][user['template_stage']]['token']] = message.text.strip()

        data = {}
        for key in user:
            if key.startswith(prefix):
                data[key.split(prefix, 1)[1]] = user[key]

        ret = await aq.aapi.set_user_details(user['uid'], data)
        if ret is not None:
            user = await db.users.find_one_and_update({'uid': user['uid']},
                                                      {'$set': {**data,
                                                                'opt_reg': user['opt_reg'],
                                                                'template_stage': 0,
                                                                'tokens': ret['template']['tokens'],
                                                                'tokens_num': len(ret['template']['tokens'])
                                                                }}, return_document=ReturnDocument.AFTER)
            user['template_stage'] = -1
            await message.answer("Ми не змогли розібрати відповідь на деякі пункти, будь ласка, дайте відповідь на них ще раз.")
            await send_token_prompt(user, message)
        else:
            await db.users.find_one_and_update({'uid': user['uid']},
                                               {'$set': {**data, 'stage': Stage.menu,
                                                         'opt_reg_completed': user['opt_reg']},
                                                '$inc': {'template_stage': 1},
                                                '$unset': {'tokens': '',
                                                           'opt_reg': ''}})

            await message.answer(
                "<b>Електронна черга ФІОТ</b>\n\nДля реєстрації у черзі на подання документів, натисніть \"Усі черги\" та оберіть необхідну вам.\n\nЯкщо у вас виникнуть якісь запитання чи проблеми, натисніть кнопку \"Допомога\" та напишіть нам про це.\n\nЯкщо ви хочете прискорити подання документів, натисніть кнопку <b>Продовжити реєстрацію</b>.",
                reply_markup=keyboards.get_menu_kbd(user['lang'], user['opt_reg']),
                parse_mode=types.ParseMode.HTML)

    async def send_token_prompt(user, message):
        kbd = None
        if 'values' in user['tokens'][user['template_stage'] + 1]:
            kbd_entries = list(map(lambda x: types.InlineKeyboardButton(text=x, callback_data=f'Token{x}'),
                                   user['tokens'][user['template_stage'] + 1]['values']))
            kbd = types.InlineKeyboardMarkup(row_width=2,
                                             inline_keyboard=list(keyboards.divide_chunks(kbd_entries, 2)))
        await message.answer(user['tokens'][user['template_stage'] + 1]['text'], reply_markup=kbd,
                             parse_mode=types.ParseMode.HTML)

    async def text_handler(message: types.Message):
        user = await db.users.find_one({'uid': message.from_user.id})

        if user is None:
            return await start_handler(message)

        elif user['stage'] == Stage.template:
            data = {('o_' if user['opt_reg'] else 't_') + user['tokens'][user['template_stage']][
                'token']: message.text.strip()}

            if 'values' in user['tokens'][user['template_stage']]:
                return await message.answer("Для відповіді на це питання використовуйте кнопки")

            if user['template_stage'] + 1 == user['tokens_num']:
                return await complete_token_registration(user, message)

            await send_token_prompt(user, message)

            await db.users.find_one_and_update({'uid': user['uid']},
                                               {'$set': {**data},
                                                '$inc': {'template_stage': 1}})

        elif user['stage'] == Stage.leave_queue:
            if message.text.strip().lower() in ['да', 'так', 'yes', 'д', 'y']:
                try:
                    await aq.aapi.remove_user_from_queue(user['leave_queue'], user['uid'])
                except KeyError:
                    pass  # ignore if already removed
                await db.users.find_one_and_update({'uid': user['uid']}, {'$set': {'stage': Stage.menu}})
                await message.answer("Ви вийшли з черги!",
                                     reply_markup=keyboards.get_menu_kbd(user['lang'], user['opt_reg_completed']),
                                     parse_mode=types.ParseMode.HTML)

    handlers = [
        {'fun': start_handler, 'named': {'commands': ['start']}},
        {'fun': help_handler, 'named': {'commands': ['info', 'help', 'support']}},
        {'fun': location_handler, 'named': {'content_types': types.ContentType.LOCATION}},
        {'fun': text_handler, 'named': {'content_types': types.ContentType.TEXT}}
    ]

    for handler in handlers:
        aq.dp.register_message_handler(handler['fun'], **handler['named'])
    aq.dp.register_callback_query_handler(query_handler)
