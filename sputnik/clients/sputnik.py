import asyncio
from dataclasses import dataclass
from datetime import datetime
from xml.etree import ElementTree

from typing import List, Dict, Tuple

from sputnik import settings
from sputnik.clients.base import BaseClient


@dataclass
class Post:
    post_id: str

    title: str
    link: str
    guid: str
    pub_date: str
    description: str
    category: str
    enclosure: str

    text: str

    short_link: str = None


class SputnikClint(BaseClient):
    async def get_rss(self):
        data = await self.get(settings.RSS_FEED)
        return data

    async def create_short_link(self, post_id):
        data = await self.get(settings.SHORT_LINK.format(post_id=post_id))
        return data


class SputnikService(SputnikClint):
    def _get_post_data(self, item: ElementTree.Element) -> Post:
        """
        Получаем данные по посту из ElementTree.Element

        :param item:
        :return:
        """
        enclosure = item.find('enclosure')

        guid = item.findtext('guid')
        post_id = [i for i in guid.split('/') if i][-1]

        return Post(
            post_id=post_id,

            title=item.findtext('title'),
            link=item.findtext('link'),
            guid=guid,
            pub_date=item.findtext('pubDate'),
            description=item.findtext('description'),
            category=item.findtext('category'),
            enclosure=enclosure.attrib.get('url') if enclosure is not None else None,

            text=ElementTree.tostring(item, encoding='UTF-8').decode('utf-8')
        )

    def _get_post_list(self, rss_text: str) -> List[Post]:
        """
        Парсит RSS XML и отдает список всех постов в dataclass

        :param rss_text:
        :return:
        """
        tree = ElementTree.fromstring(rss_text)
        return [self._get_post_data(item) for item in tree.findall('channel/item')]

    async def _get_guid_and_short_link(self, guid: str, post_id: str) -> Tuple[str, str]:
        """
        утоню для чего эта данныая функция:

        чтобы можно было обеденить guid и short_link отдаю тут эти данный,
        данная функция расчитана при исопльзовании asyncio.gather

        :param guid:
        :param post_id:
        :return:
        """
        return (
            guid, await self.get_short_link(post_id)
        )

    async def add_link_in_post(self, post_list: List[Post]):
        """
        Подмешинвает в список постов короткие ссылки, но если в посте есть guid и post_id

        :param post_list:
        :return:
        """
        # формирует список с функциями и выполняет их асинхронно
        post_ids_list = [self._get_guid_and_short_link(item.guid, item.post_id[8:]) for item in post_list]
        short_link: Dict[str, str] = dict(await asyncio.gather(*post_ids_list))

        # подемешиваем короткие ссылки в посты
        for item in post_list:
            item.short_link = short_link.get(item.guid)

    async def get_post(self, with_link: bool = False) -> List[Post]:
        """
        Получаем все посты

        :param with_link: включает получения коротких ссылок
        :return:
        """
        rss_feed = await self.get_rss()

        # получаем все посты
        post_list = self._get_post_list(rss_feed.text)

        # получаем короткие ссылки (это 150 запросов)
        if with_link:
            await self.add_link_in_post(post_list)

        return post_list

    async def get_short_link(self, post_id: str) -> str:
        """
        Получает короткую ссылку по id поста

        :param post_id:
        :return:
        """

        req = await self.create_short_link(post_id)
        return req.text