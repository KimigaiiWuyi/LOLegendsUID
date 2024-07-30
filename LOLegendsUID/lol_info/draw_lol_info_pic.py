import json
import random
from pathlib import Path
from typing import List, Union
from json import JSONDecodeError

from PIL import Image, ImageDraw
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.fonts.fonts import core_font as cf

from ..utils.lol_api import wg_api
from ..utils.error_reply import get_error
from ..utils.resource.HERO_INFO import get_hero_data
from ..utils.resource.RESOURCE_PATH import SKINS_LOADING_PATH
from ..utils.api.remote_const import LOL_TIER, LOL_QUEUE, LOL_GameArea
from ..utils.api.models import (
    Profiles,
    SkinInfo,
    SummonerInfo,
    PlayerSkinAPIResponse,
    PlayerStatsApiResponse,
    BattleReportAPIResponse,
)

TEXT_PATH = Path(__file__).parent / 'texture2d'

W = (250, 250, 250)
S = (227, 227, 227)
B = (20, 20, 20)
rgb_value = (15, 23, 36)


async def draw_lol_info_bg(profile_data: Profiles):
    '''BG'''
    card = Image.new('RGBA', (900, 900))
    card_mask = Image.open(TEXT_PATH / 'card_mask.png')

    try:
        card_bg = json.loads(profile_data['cardbg'])
        card_hero: str = card_bg['championSkin']['heroId']
        card_skin: str = card_bg['championSkin']['skinId']
    except JSONDecodeError:
        card_hero = '1'
        card_skin = '001'

    skin_id = card_skin.lstrip(card_hero)
    splash_id = f'{card_hero}-{skin_id}'

    card_img = await wg_api.get_resource('skins/splash', splash_id)
    card_img = card_img.resize((960, 540)).convert('RGBA')
    # width, height = card_img.size
    # middle_bottom_pixel = (width // 2, height - 1)
    # rgb_value = card_img.getpixel(middle_bottom_pixel)

    card.paste(card_img, (-30, 0), card_img)
    img = Image.new('RGBA', (900, 900), rgb_value)
    img.paste(card, (0, 0), card_mask)
    # (900, 900)
    return img


async def draw_lol_info_title(
    uid: str,
    info_data: SummonerInfo,
    stat_data: PlayerStatsApiResponse,
    battle_data: BattleReportAPIResponse,
    skin_data: PlayerSkinAPIResponse,
):
    '''DEAL'''
    _id, _area = uid.split(':')
    player_area = LOL_GameArea[_area]
    player_area_str = f"{player_area['name']}·Lv{info_data['level']}"
    like_and_dis = f"{info_data['praise']}赞·{info_data['discredit']}踩"
    play_times = stat_data['recent_state']['play_times']
    win_times = stat_data['recent_state']['win_times']

    mvp_times = stat_data['game_career']['total_mvp_times']
    svp_times = stat_data['game_career']['total_svp_times']

    kill8_times = stat_data['game_career']['total_god_likes']
    kill5_times = stat_data['game_career']['total_penta_kills']

    highest_score = stat_data['game_career']['highest_game_score']
    highest_score = '{:.1f}'.format(highest_score / 10000)
    skin_num = skin_data['skin_num']

    tier = battle_data['season_list'][0]['tier']
    queue = battle_data['season_list'][0]['queue']

    team_tier = battle_data['season_list'][0]['team_tier']
    team_queue = battle_data['season_list'][0]['team_queue']

    if tier != 255:
        rank = f'{LOL_TIER[tier]}·{LOL_QUEUE[queue]}'
    else:
        rank = '无段位'

    if team_tier != 255:
        team_rank = f'{LOL_TIER[team_tier]}·{LOL_QUEUE[team_queue]}'
    else:
        team_rank = '无段位'

    play_times_str = str(play_times)
    if play_times:
        win_rate = '{:.2f}%'.format((win_times / play_times) * 100)
    else:
        win_rate = 'NaN%'

    '''title'''
    title = Image.open(TEXT_PATH / 'title.png')
    title_cover = Image.open(TEXT_PATH / 'title_cover.png')

    title_draw = ImageDraw.Draw(title)

    rank_img = await wg_api.get_resource('tier', f'tier-{tier}')
    team_rank_img = await wg_api.get_resource('tier', f'tier-{team_tier}')
    icon_img = await wg_api.get_resource('usericon', info_data['icon_id'])
    icon_img = icon_img.resize((84, 84)).convert('RGBA')
    title.paste(icon_img, (54, 259), icon_img)
    title.paste(rank_img, (732, 113), rank_img)
    title.paste(team_rank_img, (572, 113), team_rank_img)

    title_draw.text((155, 285), info_data['name'], W, cf(32), 'lm')
    title_draw.text((155, 318), player_area_str, W, cf(20), 'lm')
    title_draw.text((132, 373), like_and_dis, B, cf(20), 'mm')

    title_draw.text((92, 419), play_times_str, W, cf(32), 'mm')
    title_draw.text((205, 419), win_rate, W, cf(32), 'mm')
    title_draw.text((318, 419), str(skin_num), W, cf(32), 'mm')

    title_draw.text((799, 259), rank, W, cf(32), 'mm')
    title_draw.text((639, 259), team_rank, W, cf(32), 'mm')

    title_draw.text((633, 367), str(mvp_times), B, cf(26), 'lm')
    title_draw.text((801, 367), str(svp_times), B, cf(26), 'lm')
    title_draw.text((633, 443), str(kill5_times), B, cf(26), 'lm')
    title_draw.text((801, 443), str(kill8_times), B, cf(26), 'lm')

    title.paste(title_cover, (0, 0), title_cover)
    # (900, 500)
    return title


async def draw_lol_info_img(ev: Event, uid: str) -> Union[str, bytes]:
    info_data = await wg_api.get_summoner_info(uid)
    stat_data = await wg_api.get_player_recent_stat(uid)
    battle_data = await wg_api.get_battle_report(uid)
    skin_data = await wg_api.get_player_skin_stat(uid)
    champion_data = await wg_api.get_player_champion_stat(uid)
    profile_data = await wg_api.get_player_profile(uid)

    if isinstance(info_data, int):
        return get_error(info_data)
    if isinstance(stat_data, int):
        return get_error(stat_data)
    if isinstance(battle_data, int):
        return get_error(battle_data)
    if isinstance(skin_data, int):
        return get_error(skin_data)
    if isinstance(champion_data, int):
        return get_error(champion_data)
    if isinstance(profile_data, int):
        return get_error(profile_data)

    '''DEAL'''
    play_times = stat_data['recent_state']['play_times']
    win_times = stat_data['recent_state']['win_times']

    kill5_times = stat_data['game_career']['total_penta_kills']

    kill4_times = stat_data['game_career']['total_quadra_kills']
    kill3_times = stat_data['game_career']['total_triple_kills']
    max_con_win = stat_data['game_career']['max_consecutive_wins']
    highest_score = stat_data['game_career']['highest_game_score']
    highest_score = '{:.1f}'.format(highest_score / 10000)
    most_kill = stat_data['game_career']['most_kills_num']
    most_assist = stat_data['game_career']['most_assists_num']
    most_spree_kill = stat_data['game_career']['most_spree_kills_num']
    most_damage = stat_data['game_career']['most_damage_num']
    most_damage_taken = stat_data['game_career']['most_damage_taken_num']
    most_gold = stat_data['game_career']['most_gold_earned_num']
    most_minions_kill = stat_data['game_career']['most_minions_kill_num']
    most_turrets_kill = stat_data['game_career']['most_turrets_kill_num']
    total_kills = stat_data['game_career']['total_kills']
    total_assists = stat_data['game_career']['total_assists']
    longest_game = stat_data['game_career']['longest_game_num']
    shortest_game = stat_data['game_career']['shortest_game_num']
    champion_num = skin_data['champion_num']

    kda = stat_data['recent_state']['kda']
    kda_str = '{:.1f}'.format(kda / 1000)

    match_times = battle_data['battle_count']['total_match_games']
    match_win_times = battle_data['battle_count']['total_match_wins']
    if match_times != 0:
        match_win_rate = '{:.1f}%'.format(
            (match_win_times / match_times) * 100
        )
    else:
        match_win_rate = '0.0%'

    arm_times = battle_data['battle_count']['total_arm_games']
    arm_win_times = battle_data['battle_count']['total_arm_wins']
    if arm_times != 0:
        arm_win_rate = '{:.1f}%'.format((arm_win_times / arm_times) * 100)
    else:
        arm_win_rate = '0.0%'

    rank_times = battle_data['battle_count']['total_rank_games']
    rank_win_times = battle_data['battle_count']['total_rank_wins']
    if rank_times != 0:
        rank_win_rate = '{:.1f}%'.format((rank_win_times / rank_times) * 100)
    else:
        rank_win_rate = '0.0%'

    team_times = battle_data['battle_count']['total_teamrank_games']
    team_win_times = battle_data['battle_count']['total_teamrank_wins']
    if team_times != 0:
        team_win_rate = '{:.1f}%'.format((team_win_times / team_times) * 10)
    else:
        team_win_rate = '0.0%'

    if play_times:
        win_rate = '{:.2f}%'.format((win_times / play_times) * 100)
    else:
        win_rate = 'NaN%'

    img = Image.new('RGBA', (900, 1800), rgb_value)

    bg = await draw_lol_info_bg(profile_data)
    title = await draw_lol_info_title(
        uid, info_data, stat_data, battle_data, skin_data
    )
    img.paste(bg, (0, 0), bg)
    img.paste(title, (0, 0), title)

    '''mid'''
    mid = Image.open(TEXT_PATH / 'mid.png')
    mid_draw = ImageDraw.Draw(mid)

    mid_draw.text((130, 114), kda_str, W, cf(36), 'mm')

    o = 161
    mid_draw.text((130 + o, 114), match_win_rate, W, cf(36), 'mm')
    mid_draw.text((130 + o, 150), str(match_times) + '场', S, cf(22), 'mm')

    mid_draw.text((130 + o * 2, 114), arm_win_rate, W, cf(36), 'mm')
    mid_draw.text((130 + o * 2, 150), str(arm_times) + '场', S, cf(22), 'mm')

    mid_draw.text((130 + o * 3, 114), rank_win_rate, W, cf(36), 'mm')
    mid_draw.text((130 + o * 3, 150), str(rank_times) + '场', S, cf(22), 'mm')

    mid_draw.text((130 + o * 4, 114), team_win_rate, W, cf(36), 'mm')
    mid_draw.text((130 + o * 4, 150), str(team_times) + '场', S, cf(22), 'mm')
    img.paste(mid, (0, 485), mid)

    '''DATA'''
    data = Image.open(TEXT_PATH / 'data.png')
    data_draw = ImageDraw.Draw(data)
    for index, msg in enumerate(
        [
            kill5_times,
            kill4_times,
            kill3_times,
            max_con_win,
            highest_score,
            most_kill,
            most_assist,
            most_spree_kill,
            most_damage,
            most_damage_taken,
            most_gold,
            most_minions_kill,
            most_turrets_kill,
            total_kills,
            total_assists,
            longest_game,
            shortest_game,
            champion_num,
        ]
    ):
        xy = (114 + 135 * (index % 6), 75 + 103 * (index // 6))
        data_draw.text(xy, str(msg), W, cf(32), 'mm')
    img.paste(data, (0, 650), data)

    '''CHAMPION'''
    champion_bar = Image.open(TEXT_PATH / 'champion_bar.png')
    img.paste(champion_bar, (0, 1018), champion_bar)

    sorted_champion = sorted(
        champion_data, key=lambda x: x['used_exp'], reverse=True
    )
    champion_card = Image.open(TEXT_PATH / 'champion_card.png')
    for ci, champion in enumerate(sorted_champion[:5]):
        champion_id = champion['champion_id']
        hero_data = await get_hero_data(champion_id)
        champion_img = await wg_api.get_resource('card', champion_id)
        champion_img = champion_img.resize((180, 327))
        champion_img.paste(champion_card, (0, 0), champion_card)
        champion_draw = ImageDraw.Draw(champion_img)

        champion_name = hero_data['hero']["name"]
        exp = str(champion['used_exp'])
        total = champion['total']
        wins = champion['wins']
        if not total:
            win_rate = '{:.1f}%'.format((wins / total) * 100)
            win_str = f'{win_rate} / {total}场'
        else:
            win_str = 'NaN%'

        champion_draw.text((90, 210), champion_name, W, cf(26), 'mm')
        champion_draw.text((90, 270), exp, (255, 210, 150), cf(28), 'mm')
        champion_draw.text((90, 300), win_str, S, cf(18), 'mm')

        if ci < 3:
            rank_icon = Image.open(TEXT_PATH / f'rank_icon{ci+1}.png')
            rank_icon = rank_icon.resize((32, 35))
            champion_img.paste(rank_icon, (5, 5), rank_icon)

        champion_img = champion_img.resize((140, 255)).convert('RGBA')
        img.paste(champion_img, (59 + ci * 161, 1080), champion_img)

    '''SKIN'''
    skin_bar = Image.open(TEXT_PATH / 'skin_bar.png')
    img.paste(skin_bar, (0, 1360), skin_bar)

    skin_list: List[SkinInfo] = []
    for i in skin_data['championSkins']:
        if not i['skins']:
            continue
        skins = []
        for s in i['skins']:
            s['hero_id'] = i['id']
            if s['chromas'] == 0:
                skins.append(s)
        skin_list.extend(skins)
    random.shuffle(skin_list)

    skin_card = Image.open(TEXT_PATH / 'skin_card.png')
    for si, skin in enumerate(skin_list[:5]):
        hero_data = await get_hero_data(skin['hero_id'])
        skin_name = '未知皮肤'
        skin_img = ''
        for i in hero_data['skins']:
            if str(i['skinId']) == str(skin['id']):
                if i['chromas'] == '0':
                    skin_name = i['name']
                    skin_img = i['loadingImg']
                    break
                else:
                    _new_name: List = i['name'].split(' ')
                    _new_name.pop()
                    new_name = ' '.join(_new_name)
                    for d in hero_data['skins']:
                        if new_name == d['name']:
                            skin_name = d['name']
                            skin_img = d['loadingImg']
                            break
                    break

        # instance_id = skin['instance_id']
        # loading_img = await wg_api.get_resource('skins/loading', instance_id)

        loading_img = await wg_api.get_image(
            skin_img, SKINS_LOADING_PATH, skin_img.split('/')[-1]
        )
        loading_img = loading_img.resize((308, 560))
        loading_img.paste(skin_card, (0, 0), skin_card)

        loading_draw = ImageDraw.Draw(loading_img)
        loading_draw.text((154, 492), skin_name, (255, 201, 150), cf(32), 'mm')

        loading_img = loading_img.resize((140, 255)).convert('RGBA')
        img.paste(loading_img, (59 + si * 161, 1428), loading_img)

    '''FOOTER'''
    footer = Image.open(TEXT_PATH / 'footer.png')
    img.paste(footer, (0, 1745), footer)

    return await convert_img(img)
