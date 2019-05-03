import asyncio

from sputnik.clients.base import BaseClient
from sputnik.clients.file_download import download_img
from sputnik.settings import ANTI_CAPTCHA_KEY


class AntiCaptchaClient(BaseClient):
    BASE_URL = 'https://api.anti-captcha.com/'
    VERIFY_SSL = False

    TOKEN = ANTI_CAPTCHA_KEY

    create_task_url = 'createTask'
    get_task_url = 'getTaskResult'

    async def crete_captcha_task(self, captcha_data):
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

    async def get_recaptcha_in_url(self, data, download_captcha=True):
        if download_captcha:
            data = await download_img(data, self.TIMEOUT)

        task = await self.crete_captcha_task(data)

        task_id = task.json['taskId']

        # todo нужон перейти на время
        for _ in range(10):
            await asyncio.sleep(0.5)
            recaptcha = await self.get_task(task_id)
            if recaptcha.json['status'] == 'ready':
                return recaptcha.json['solution']['text']
        return None
