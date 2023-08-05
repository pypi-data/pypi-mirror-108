from typing import Any
import httpx
import json

from .platform import PlatformNoTarget
from ..utils import Singleton
from ..types import RawPost
from ..post import Post

class MonsterSiren(PlatformNoTarget):

    categories = {}
    platform_name = 'monster-siren'
    enable_tag = False
    enabled = True
    is_common = False
    schedule_interval = 30
    name = '塞壬唱片官网新闻'

    @staticmethod
    async def get_account_name(_) -> str:
        return '塞壬唱片新闻'

    async def get_sub_list(self) -> list[RawPost]:
        async with httpx.AsyncClient() as client:
            raw_data = await client.get('https://monster-siren.hypergryph.com/api/news')
            return raw_data.json()['data']['list']

    def get_id(self, post: RawPost) -> Any:
        return post['cid']

    def get_date(self, _) -> None:
        return None

    async def parse(self, raw_post: RawPost) -> Post:
        url = f'https://monster-siren.hypergryph.com/info/{raw_post["cid"]}'
        return Post('monster-siren', text=raw_post['title'],
                url=url, target_name="塞壬唱片新闻", compress=True,
                override_use_pic=False)
