import json
import json as js
import urllib.parse
from pathlib import Path
from copy import deepcopy
from typing import Any, Dict, List, Union, Literal, Optional, cast

import aiofiles
from PIL import Image
from aiohttp import FormData
from httpx import AsyncClient
from gsuid_core.logger import logger
from gsuid_core.utils.download_resource.download_file import download

from ..database.models import LOLUser
from ..resource.RESOURCE_PATH import (
    CARD_PATH,
    HERO_LIST,
    TIER_PATH,
    ITEMS_PATH,
    RESOURCE_PATH,
    USERICON_PATH,
    CHAMPIONS_PATH,
    HERO_DATA_PATH,
    RUNESPERK_PATH,
    SKINS_SPLASH_PATH,
    SKINS_LOADING_PATH,
    SUMMONABILITY_PATH,
    SKINS_ORIGINAL_PATH,
)
from .models import (
    Profiles,
    BattleInfo,
    PlayerInfo,
    BattleDetail,
    ChampionInfo,
    SummonerInfo,
    UserSnapshot,
    TFTBattleList,
    TFTGameCareer,
    TFTBattleDetail,
    TFTBattleReport,
    PlayerSkinAPIResponse,
    PlayerStatsApiResponse,
    BattleReportAPIResponse,
)
from .api import (
    IMG_BASE,
    HERO_DETAIL,
    HERO_LIST_API,
    ResAPI,
    SearchAPI,
    SummonerAPI,
    BattleListAPI,
    PlayerSkinAPI,
    SkinLoadingAPI,
    BattleDetailAPI,
    BattleReportAPI,
    PlayerRecentAPI,
    UserSnapshotAPI,
    PlayerProfileAPI,
    TFTBattleListAPI,
    TFTGameCareerAPI,
    PlayerChampionAPI,
    TFTBattleDetailAPI,
    TFTBattleReportAPI,
)


class WeGameApi:
    ssl_verify = False
    _HEADER: Dict[str, str] = {
        'Referer': 'https://www.wegame.com.cn/helper/lol/v2/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/91.0.4472.164'
        'Safari/537.36 qblink wegame.exe'
        ' WeGame/5.6.6.12275 ChannelId/0'
        'QBCore/91.1.23+g04c8d56+chromium-91.0.4472.164'
        'QQBrowser/9.0.2524.400',
        'HOST': 'www.wegame.com.cn',
        # 'trpc-caller': 'wegame.pallas.web.LolBattle',
    }

    async def search_player(
        self,
        player_name: str,
    ):
        data = await self._wg_request(
            SearchAPI,
            json={'nickname': player_name, 'from_src': 'lol_helper'},
        )
        if isinstance(data, int):
            return data
        return cast(List[PlayerInfo], data['players'])

    async def get_summoner_info(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            SummonerAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'from_src': 'tft_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(SummonerInfo, data['summoner'])

    async def get_battle_list(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            BattleListAPI,
            json={
                'account_type': 2,
                'area': area,
                'id': uid,
                'count': 8,
                'filter': '',
                'offset': 0,
                'from_src': 'lol_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(List[BattleInfo], data['battles'])

    async def get_player_recent_stat(
        self, uid: str, area: Optional[int] = None
    ):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            PlayerRecentAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'from_src': 'lol_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(PlayerStatsApiResponse, data)

    async def get_player_champion_stat(
        self, uid: str, area: Optional[int] = None
    ):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            PlayerChampionAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'from_src': 'lol_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(List[ChampionInfo], data['champion_list'])

    async def get_player_skin_stat(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            PlayerSkinAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'from_src': 'lol_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(PlayerSkinAPIResponse, data)

    async def get_battle_report(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            BattleReportAPI,
            json={
                'account_type': 2,
                'area': area,
                'id': uid,
                'sids': [255],
                'from_src': 'lol_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(BattleReportAPIResponse, data)

    async def get_battle_detail(
        self, uid: str, game_id: str, area: Optional[int] = None
    ):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            BattleDetailAPI,
            json={
                'account_type': 2,
                'area': area,
                'id': uid,
                'game_id': game_id,
                'from_src': 'lol_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(BattleDetail, data['battle_detail'])

    async def get_player_profile(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            PlayerProfileAPI,
            json={
                "account_type": 2,
                "area": area,
                "id": uid,
                "fields": [
                    "tag",
                    "cardbg",
                    "skincabinet",
                    "skincabinetshow",
                    "label",
                    "showExpType",
                ],
                "from_src": "lol_helper",
            },
        )
        if isinstance(data, int):
            return data
        return cast(Profiles, data['profiles'])

    async def get_user_snapshot(
        self, uid: str, game_id: str, area: Optional[int] = None
    ):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            UserSnapshotAPI,
            json={
                'account_type': 2,
                'action_type': 0,
                'area': area,
                'id': uid,
                'limit': 3,
                'offset': 0,
                'from_src': 'lol_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(List[UserSnapshot], data['snapshots'])

    async def get_tft_gamecareer(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            TFTGameCareerAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'from_src': 'tft_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(TFTGameCareer, data['game_career'])

    async def get_tft_battle_list(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            TFTBattleListAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'offset': 0,
                'count': 7,
                'filter': 'all',
                'from_src': 'tft_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(List[TFTBattleList], data['battles'])

    async def get_tft_battle_report(
        self, uid: str, area: Optional[int] = None
    ):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            TFTBattleReportAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'from_src': 'tft_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(TFTBattleReport, data)

    async def get_tft_battle_detail(
        self, uid: str, game_id: Union[str, int], area: Optional[int] = None
    ):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            TFTBattleDetailAPI,
            json={
                'account_type': 2,
                'id': uid,
                'area': area,
                'game_id': int(game_id),
                'from_src': 'tft_helper',
            },
        )
        if isinstance(data, int):
            return data
        return cast(TFTBattleDetail, data['battle_detail'])

    async def get_hero_list(self):
        data = await self._help_request(
            HERO_LIST_API,
            False,
        )
        if isinstance(data, int):
            return data
        data = json.dumps(data, ensure_ascii=False, indent=2)
        async with aiofiles.open(HERO_LIST, 'w', encoding='utf-8') as file:
            await file.write(data)

    async def get_hero_info(self, hero_id: Union[str, int]):
        data = await self._help_request(HERO_DETAIL.format(hero_id))
        if isinstance(data, int):
            return data
        data = json.dumps(data, ensure_ascii=False, indent=2)
        async with aiofiles.open(
            HERO_DATA_PATH / f'{hero_id}.json', 'w', encoding='utf-8'
        ) as file:
            await file.write(data)

    async def get_resource(
        self,
        type: Literal[
            'items',
            'card',
            'runesperk',
            'skins/splash',
            'skins/original',
            'skins/loading',
            'usericon',
            'champions',
            'summonability',
            'tier',
        ],
        resource_id: Union[str, int],
        download_to: Optional[Path] = None,
    ) -> Image.Image:
        if type in ['skins/splash', 'skins/original', 'skins/loading', 'card']:
            suffix = 'jpg'
        else:
            suffix = 'png'
        FILE_NAME = f'{resource_id}.{suffix}'

        if type == 'tier':
            URL = f'{IMG_BASE}/lol/v2/tier/{FILE_NAME}'
        elif type == 'skins/loading':
            URL = f'{SkinLoadingAPI}/{FILE_NAME}'
        else:
            URL = f'{ResAPI}/{type}/{FILE_NAME}'

        if download_to is None:
            if type == 'skins/splash':
                download_to = SKINS_SPLASH_PATH
            elif type == 'skins/original':
                download_to = SKINS_ORIGINAL_PATH
            elif type == 'card':
                download_to = CARD_PATH
            elif type == 'usericon':
                download_to = USERICON_PATH
            elif type == 'champions':
                download_to = CHAMPIONS_PATH
            elif type == 'summonability':
                download_to = SUMMONABILITY_PATH
            elif type == 'runesperk':
                download_to = RUNESPERK_PATH
            elif type == 'items':
                download_to = ITEMS_PATH
            elif type == 'tier':
                download_to = TIER_PATH
            elif type == 'skins/loading':
                download_to = SKINS_LOADING_PATH
            else:
                download_to = RESOURCE_PATH

        return await self.get_image(URL, download_to, FILE_NAME)

    async def get_image(self, URL: str, download_to: Path, FILE_NAME: str):
        if not URL:
            return Image.new('RGBA', (128, 128))

        if not (download_to / FILE_NAME).exists():
            await download(URL, download_to, FILE_NAME, None, '[LOLegendsUID]')

        if (download_to / FILE_NAME).exists():
            return Image.open(download_to / FILE_NAME)
        else:
            return Image.new('RGBA', (128, 128))

    async def _help_request(
        self, url: str, is_log: bool = True
    ) -> Union[Dict, int]:
        try:
            async with AsyncClient(verify=False) as session:
                data = await session.get(url)
                d = data.text
                if is_log:
                    logger.debug(d)
                return json.loads(d)
        except:  # noqa:E722
            return -500

    async def _wg_request(
        self,
        url: str,
        method: Literal['GET', 'POST'] = 'GET',
        header: Dict[str, str] = _HEADER,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[FormData] = None,
        need_ck: bool = True,
    ) -> Union[Dict, int]:
        header = deepcopy(self._HEADER)
        if url == SearchAPI and json:
            BASE = 'https://www.wegame.com.cn/helper/lol/search/index.html'
            kw = urllib.parse.quote_plus(json["nickname"])
            header['Referer'] = f'{BASE}?kw={kw}&navid=61'

        if need_ck and 'Cookie' not in header:
            if json and 'id' in json:
                uid = json['id']
            else:
                uid = ' 9999'
            ck = await LOLUser.get_random_cookie(uid)
            if ck:
                header['Cookie'] = ck
            else:
                return -511

        if json:
            method = 'POST'

        async with AsyncClient(verify=self.ssl_verify) as client:
            resp = await client.request(
                method,
                url=url,
                headers=header,
                params=params,
                json=json,
                timeout=300,
            )
            try:
                raw_data = await resp.json()
            except:  # noqa: E722
                _raw_data = resp.text
                try:
                    raw_data = js.loads(_raw_data)
                except:  # noqa: E722
                    raw_data = {
                        'result': {'error_code': -999, 'data': _raw_data}
                    }
            logger.debug(raw_data)
            if (
                'result' in raw_data
                and 'error_code' in raw_data['result']
                and raw_data['result']['error_code'] != 0
            ):
                return raw_data['result']['error_code']
            return raw_data
