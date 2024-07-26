from functools import partial

from aiogram import Dispatcher, Bot
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.middlewares.authentication import verify_token
from app.api.routes.main import main_router
from app.api.routes.webhook import webhook_router
from app.api.stubs import BotStub, DispatcherStub, SecretStub
from app.settings import settings


async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        settings.WEBHOOK_URL,
        drop_pending_updates=True,
        secret_token=settings.TELEGRAM_SECRET.get_secret_value()
    )


async def on_shutdown(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)


def create_app(bot: Bot, dispatcher: Dispatcher, webhook_secret: str) -> FastAPI:
    app = FastAPI()

    app.dependency_overrides.update(
        {
            BotStub: lambda: bot,
            DispatcherStub: lambda: dispatcher,
            SecretStub: lambda: webhook_secret,
        }
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler('startup', partial(on_startup, bot))
    app.add_event_handler('shutdown', partial(on_shutdown, bot))
    app.include_router(webhook_router)

    api = APIRouter(dependencies=[Depends(verify_token)])

    api.include_router(main_router)

    app.include_router(api)

    return app
