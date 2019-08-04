from typing import Union
from dataclasses import dataclass


@dataclass
class PostStatus:
    is_send_telegram: bool
    is_send_weibo: bool


@dataclass
class PostResponse:

    id: int
    link: str
    short_link: str

    photo: str

    text: str
    title: str

    created_at: str
    status: Union[dict, PostStatus]
