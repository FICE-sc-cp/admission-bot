from app.bot.admission_api.base import BaseAPI


class TemplateAPI(BaseAPI):
    _path = "/templates"

    async def get_registration_template(self):
        async with self._session.get(f'{self.path}/templates/registration') as resp:
            return await resp.json()
