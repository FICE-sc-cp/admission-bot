from typing import Any

from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from email_validator import validate_email, EmailNotValidError
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, RequestLocation, RequestContact, Next, Button, Row, SwitchTo
from aiogram_dialog.widgets.kbd.select import OnItemClick, Radio, Multiselect
from aiogram_dialog.widgets.text import Const, Format

from app.bot.states.form import Form
from app.types.confirms import Confirms
from app.types.specialities import Specialities


class OnSelectHostel(OnItemClick[Any, Confirms]):
    async def __call__(self, event: CallbackQuery, select: Any, dialog_manager: DialogManager, data: Confirms) -> None:
        dialog_manager.dialog_data["hostel"] = data
        await dialog_manager.next()


class OnSelectEdbo(OnItemClick[Any, Confirms]):
    async def __call__(self, event: CallbackQuery, select: Any, dialog_manager: DialogManager, data: Confirms) -> None:
        dialog_manager.dialog_data["edbo"] = data
        await dialog_manager.next()


async def specialty_handler(event: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    specialities = dialog_manager.find("specialty").get_checked()
    if len(specialities) == 0:
        await event.answer("Оберіть хочаб одну спеціальність")
    else:
        dialog_manager.dialog_data["specialities"] = ", ".join(specialities)
        await dialog_manager.switch_to(Form.contact)


async def email_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    try:
        validate_email(message.text)
    except EmailNotValidError as e:
        await message.answer("Неправильно введена пошта. Спробуйте ще раз")
    else:
        await manager.next()


async def location_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    print(message.location)
    await manager.next()


async def contact_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    manager.dialog_data["phone"] = message.contact.phone_number
    await manager.next()


async def get_data(dialog_manager: DialogManager, **kwargs):
    print(kwargs)
    return dialog_manager.dialog_data


confirm_form_message = Format("""
Перевірте введені дані
        
<b>Чи плануєте ви селитися у гуртожитку?</b> <code>{hostel}</code>
<b>Чи є у вас роздрукована заява з ЄДЕБО?</b> <code>{edbo}</code>
<b>Обрані спеціальності:</b> <code>{specialities}</code>
<b>Телефон</b> <code>{phone}</code>
""")

form = Dialog(
    Window(
        Const("Введіть пошту з якою ви реєструвалися на сайті"),
        MessageInput(email_handler, content_types=[ContentType.TEXT]),
        state=Form.email
    ),
    Window(
        Const("Чи плануєте ви селитися у гуртожитку?"),
        Select(
            text=Format("{item.value}"),
            items=list(Confirms),
            item_id_getter=lambda x: x.value,
            on_click=OnSelectHostel(),
            id="hostel"
        ),
        state=Form.hostel
    ),
    Window(
        Const("Чи є у вас роздрукована заява з ЄДЕБО?"),
        Select(
            text=Format("{item.value}"),
            items=list(Confirms),
            item_id_getter=lambda x: x.value,
            on_click=OnSelectEdbo(),
            id="edbo"
        ),
        state=Form.edbo
    ),
    Window(
        Const("Оберіть спеціальності на які плануєте вступати"),
        Multiselect(
            checked_text=Format("✓ {item.value}"),
            unchecked_text=Format("{item.value}"),
            items=list(Specialities),
            item_id_getter=lambda x: x.value,
            id="specialty"
        ),
        Button(
            Const("Далі"),
            on_click=specialty_handler,
            id="specialty_next"
        ),
        state=Form.speciality
    ),
    Window(
        Const("Поділіться своїм номером телефона"),
        RequestContact(Const("📍 Надіслати")),
        MessageInput(contact_handler, content_types=[ContentType.CONTACT]),
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
        ),
        state=Form.contact
    ),
    Window(
        confirm_form_message,
        Row(
            SwitchTo(
                text=Const("Заповнити ще раз"),
                id="resetform",
                state=Form.hostel
            ),
            Next(Const("Все вірно"))
        ),
        getter=get_data,
        state=Form.confirm
    ),
    Window(
        Const("Надішліть свою геолокацію"),
        RequestLocation(Const("📍 Надіслати")),
        MessageInput(location_handler, content_types=[ContentType.LOCATION]),
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
        ),
        state=Form.geo
    )
)
