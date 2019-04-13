import asyncio
import base64

import aiohttp
import async_timeout

from sputnik.clients.base import BaseClient
from sputnik.settings import ANTI_CAPTCHA_KEY


class AntiCaptchaClient(BaseClient):
    BASE_URL = 'https://api.anti-captcha.com/'
    VERIFY_SSL = False

    TOKEN = ANTI_CAPTCHA_KEY

    create_task_url = 'createTask'
    get_task_url = 'getTaskResult'

    async def crete_captcha_task(self, captcha_url):
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
            with async_timeout.timeout(self.TIMEOUT):
                async with session.get(url=captcha_url) as response:
                    captcha_image = await response.read()

        captcha_data = base64.b64encode(captcha_image)

        response = await self.post(
            url=self._get_url('create_task_url'),
            json={
                "clientKey": self.TOKEN,
                "task":
                    {
                        "type": "ImageToTextTask",
                        # Содержимое файла капчи закодированное в base64.
                        # Убедитесь что шлете его без переносов строки.
                        "body": captcha_data.decode('utf-8'),
                        # false - нет требований
                        # true - работник должен ввести текст с одним или
                        #  несколькими пробелами
                        "phrase": False,
                        # false - нет требований
                        # true - работник увидит специальный сигнал что
                        # ответ необходимо вводить с учетом регистра
                        "case": False,
                        # 0 - нет требований
                        # 1 - можно вводить только цифры
                        # 2 - вводить можно любые символы кроме цифр
                        # "numeric": 0,
                        # false - нет требований
                        # true - работник увидит специальный сигнал что на
                        # капче изображено математическое выражение
                        # и необходимо ввести на него ответ
                        "math": 0,
                        # 0 - нет требований
                        # > 1 - определяет минимальную длину ответа
                        "minLength": 0,
                        # 0 - нет требований
                        # > 1 - определяет максимальную длину ответа
                        "maxLength": 0
                    }
            })
        return response

    async def get_task(self, task_id):
        response = await self.post(self._get_url('get_task_url'),
                                   json={
                                       "clientKey": self.TOKEN,
                                       "taskId": task_id
                                   }
                                   )
        return response


class AntiCaptchaService(AntiCaptchaClient):

    async def get_recaptcha_in_url(self, captcha_url):
        task = await self.crete_captcha_task(captcha_url)

        task_id = task.json['taskId']

        # todo нужон перейти на время
        for _ in range(10):
            await asyncio.sleep(0.5)
            recaptcha = await self.get_task(task_id)
            if recaptcha.json['status'] == 'ready':
                return recaptcha.json['solution']['text']
        return None
