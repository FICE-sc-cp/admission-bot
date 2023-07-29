import asyncio
import logging
import typing

from aiogram import Bot, types
from aiogram.types import base
from aiogram.utils import exceptions

from timer import Timer


class SafeBot(Bot):
    def __init__(self, token):
        self._events = []
        self._reqs_per_second = 30

        async def event_scheduler():
            try:
                await self._events.pop(0)
            except IndexError:
                pass
            except exceptions.MessageNotModified:
                pass  # ignore, most probably because of queries
            except Exception as e:
                logging.error(f'Exception in event scheduler: {e}')

        self._scheduler = Timer(1 / self._reqs_per_second, event_scheduler, infinite=True, immediate=True)
        super().__init__(token)

    async def edit_message_text(self,
                                text: base.String,
                                chat_id: typing.Union[base.Integer, base.String, None] = None,
                                message_id: typing.Optional[base.Integer] = None,
                                inline_message_id: typing.Optional[base.String] = None,
                                parse_mode: typing.Optional[base.String] = None,
                                entities: typing.Optional[typing.List[types.MessageEntity]] = None,
                                disable_web_page_preview: typing.Optional[base.Boolean] = None,
                                reply_markup: typing.Union[types.InlineKeyboardMarkup, None] = None):
        self._events.append(super(SafeBot, self).edit_message_text(text,
                                                                   chat_id,
                                                                   message_id,
                                                                   inline_message_id,
                                                                   parse_mode,
                                                                   entities,
                                                                   disable_web_page_preview,
                                                                   reply_markup))

    async def send_message(self,
                           chat_id: typing.Union[base.Integer, base.String],
                           text: base.String,
                           parse_mode: typing.Optional[base.String] = None,
                           entities: typing.Optional[typing.List[types.MessageEntity]] = None,
                           disable_web_page_preview: typing.Optional[base.Boolean] = None,
                           message_thread_id: typing.Optional[base.Integer] = None,
                           disable_notification: typing.Optional[base.Boolean] = None,
                           protect_content: typing.Optional[base.Boolean] = None,
                           reply_to_message_id: typing.Optional[base.Integer] = None,
                           allow_sending_without_reply: typing.Optional[base.Boolean] = None,
                           reply_markup: typing.Union[types.InlineKeyboardMarkup,
                           types.ReplyKeyboardMarkup,
                           types.ReplyKeyboardRemove,
                           types.ForceReply, None] = None
                           ):
        self._events.append(self._send_message(chat_id, text, parse_mode, disable_web_page_preview, message_thread_id,
                                               disable_notification, reply_to_message_id, reply_markup))

    async def _send_message(self, chat_id, text, parse_mode=None, disable_web_page_preview=None, message_thread_id=None,
                            disable_notification=None, reply_to_message_id=None, reply_markup=None):
        log = logging.getLogger('bot')
        try:
            await super(SafeBot, self).send_message(chat_id, text, parse_mode, disable_web_page_preview,
                                                    message_thread_id,
                                                    disable_notification, reply_to_message_id, reply_markup)
        except exceptions.BotBlocked:
            log.error(f"Target [ID:{chat_id}]: blocked by user")
        except exceptions.ChatNotFound:
            log.error(f"Target [ID:{chat_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            return await self.send_message(chat_id, text, parse_mode, disable_web_page_preview, message_thread_id,
                                           disable_notification, reply_to_message_id, reply_markup)  # Recursive call
        except exceptions.UserDeactivated:
            log.error(f"Target [ID:{chat_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            log.exception(f"Target [ID:{chat_id}]: failed")
        else:
            # log.info(f"Target [ID:{user_id}]: success")
            return True
        return False
