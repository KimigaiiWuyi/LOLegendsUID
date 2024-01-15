from typing import Any, Dict, List, Union, Literal, Optional, cast

from gsuid_core.logger import logger
from aiohttp import FormData, TCPConnector, ClientSession, ContentTypeError

from .api import (
    SearchAPI,
    SummonerAPI,
    BattleListAPI,
    PlayerSkinAPI,
    BattleDetailAPI,
    BattleReportAPI,
    PlayerRecentAPI,
    UserSnapshotAPI,
    PlayerChampionAPI,
)
from .models import (
    BattleInfo,
    PlayerInfo,
    BattleDetail,
    ChampionInfo,
    SummonerInfo,
    UserSnapshot,
    PlayerSkinAPIResponse,
    PlayerStatsApiResponse,
    BattleReportAPIResponse,
)


class WeGameApi:
    ssl_verify = True
    _HEADER: Dict[str, str] = {}

    async def search_player(
        self,
        player_name: str,
    ):
        data = await self._wg_request(
            SearchAPI,
            json={"nickname": player_name, "from_src": "lol_helper"},
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
                "account_type": 2,
                "id": uid,
                "area": area,
                "from_src": "tft_helper",
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
                "account_type": 2,
                "area": area,
                "id": uid,
                "count": 8,
                "filter": "",
                "offset": 0,
                "from_src": "lol_helper",
            },
        )
        if isinstance(data, int):
            return data
        return cast(List[BattleInfo], data['summoner'])

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
                "account_type": 2,
                "id": uid,
                "area": area,
                "from_src": "lol_helper",
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
                "account_type": 2,
                "id": uid,
                "area": area,
                "from_src": "lol_helper",
            },
        )
        if isinstance(data, int):
            return data
        return cast(List[ChampionInfo], data["champion_list"])

    async def get_player_skin_stat(self, uid: str, area: Optional[int] = None):
        if ':' in uid:
            uid_data = uid.split(':')
            uid, area = uid_data[0], int(uid_data[1])

        if area is None:
            return -1

        data = await self._wg_request(
            PlayerSkinAPI,
            json={
                "account_type": 2,
                "id": uid,
                "area": area,
                "from_src": "lol_helper",
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
                "account_type": 2,
                "area": area,
                "id": uid,
                "sids": [255],
                "from_src": "lol_helper",
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
                "account_type": 2,
                "area": area,
                "id": uid,
                "game_id": game_id,
                "from_src": "lol_helper",
            },
        )
        if isinstance(data, int):
            return data
        return cast(BattleDetail, data['battle_detail'])

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
                "account_type": 2,
                'action_type': 0,
                "area": area,
                "id": uid,
                "limit": 3,
                'offset': 0,
                "from_src": "lol_helper",
            },
        )
        if isinstance(data, int):
            return data
        return cast(List[UserSnapshot], data['snapshots'])

    async def _wg_request(
        self,
        url: str,
        method: Literal["GET", "POST"] = "GET",
        header: Dict[str, str] = _HEADER,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[FormData] = None,
    ) -> Union[Dict, int]:
        async with ClientSession(
            connector=TCPConnector(verify_ssl=self.ssl_verify)
        ) as client:
            async with client.request(
                method,
                url=url,
                headers=header,
                params=params,
                json=json,
                data=data,
                timeout=300,
            ) as resp:
                try:
                    raw_data = await resp.json()
                except ContentTypeError:
                    _raw_data = await resp.text()
                    raw_data = {"retcode": -999, "data": _raw_data}
                logger.debug(raw_data)
                if (
                    'result' in raw_data
                    and 'error_code' in raw_data['result']
                    and raw_data['result']['error_code'] != 0
                ):
                    return raw_data['result']['error_code']
                return raw_data
