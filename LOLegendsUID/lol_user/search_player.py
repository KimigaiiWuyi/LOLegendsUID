from ..utils.lol_api import wg_api
from ..utils.api.remote_const import LOL_TIER, LOL_QUEUE, LOL_GameArea

'''Wuyi无疑 (华贵铂金·I)
区服：电信一·艾欧尼亚
等级：{}
UID: {}'''

SAMPLE = '''{} ({})
区服：{}
等级：{}
UID：{}'''


async def search_player_with_name(name: str):
    data = await wg_api.search_player(name)
    if isinstance(data, int):
        return data

    result = {}
    for player in data[:5]:
        player_uid = player['openid']
        player_rank = (
            f"{LOL_TIER[player['tier']]}·{LOL_QUEUE[player['queue']]}"
            if player['tier'] != 255
            else '无段位'
        )
        player_level = player['level']
        player_area = LOL_GameArea[str(player['area'])]
        player_area_str = f"{player_area['isp']} {player_area['name']}"
        real_uid = f'{player_uid}:{player["area"]}'
        result[real_uid] = SAMPLE.format(
            name, player_rank, player_area_str, player_level, real_uid
        )

    return result
