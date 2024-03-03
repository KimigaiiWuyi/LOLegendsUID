from typing import Union
from datetime import datetime, timezone

from PIL import Image, ImageDraw
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.fonts.fonts import core_font as cf

from ..utils.lol_api import wg_api
from ..utils.error_reply import get_error
from .draw_lol_info_pic import (
    TEXT_PATH,
    S,
    rgb_value,
    draw_lol_info_bg,
    draw_lol_info_title,
)

team_a_icon = Image.open(TEXT_PATH / "team_a_icon.png")
team_b_icon = Image.open(TEXT_PATH / "team_b_icon.png")
svp = Image.open(TEXT_PATH / "svp.png")
mvp = Image.open(TEXT_PATH / "mvp.png")


async def draw_lol_battle_list_img(ev: Event, uid: str) -> Union[str, bytes]:
    info_data = await wg_api.get_summoner_info(uid)
    stat_data = await wg_api.get_player_recent_stat(uid)
    battle_data = await wg_api.get_battle_report(uid)
    skin_data = await wg_api.get_player_skin_stat(uid)
    profile_data = await wg_api.get_player_profile(uid)
    battle_list_data = await wg_api.get_battle_list(uid)

    if isinstance(info_data, int):
        return get_error(info_data)
    if isinstance(stat_data, int):
        return get_error(stat_data)
    if isinstance(battle_data, int):
        return get_error(battle_data)
    if isinstance(skin_data, int):
        return get_error(skin_data)
    if isinstance(profile_data, int):
        return get_error(profile_data)
    if isinstance(battle_list_data, int):
        return get_error(battle_list_data)

    _id, _area = uid.split(':')
    print(f'玩家ID：{_id}')
    bg = await draw_lol_info_bg(profile_data)
    title = await draw_lol_info_title(
        uid, info_data, stat_data, battle_data, skin_data
    )

    if len(battle_list_data) >= 6:
        h = 2000 + 60
    else:
        h = len(battle_list_data) * 250 + 500 + 40

    img = Image.new('RGBA', (900, h), rgb_value)
    img.paste(bg, (0, 0), bg)
    img.paste(title, (0, 0), title)

    for index, battle in enumerate(battle_list_data[:6]):
        me_icon = Image.new('RGBA', (100, 100), rgb_value)
        game_id = battle['game_id']
        game_start_time = int(battle['game_start_time'])
        normal_datetime = datetime.fromtimestamp(
            game_start_time / 1000.0, tz=timezone.utc
        )
        formatted_date = normal_datetime.strftime("%m-%d")

        is_win = True if battle['win'] == 'Win' else False

        if is_win:
            battle_bg = Image.open(TEXT_PATH / 'win_bg.png')
            result_str = '游戏胜利'
            result_color = (64, 181, 197)
        else:
            battle_bg = Image.open(TEXT_PATH / 'fail_bg.png')
            result_str = '游戏失败'
            result_color = (241, 87, 87)

        detail = await wg_api.get_battle_detail(uid, game_id)

        if isinstance(detail, int):
            continue

        for i, team in enumerate(detail['team_details']):
            team_elo = team['teamElo']
            team_gold = team['totalGoldEarned']
            team_word = Image.open(TEXT_PATH / "team_word.png")
            team_draw = ImageDraw.Draw(team_word)
            team_draw.text((98, 20), f'{team_elo}', 'white', cf(25), 'lm')
            team_draw.text((106, 55), f'{team_gold}', 'white', cf(25), 'lm')
            battle_bg.paste(team_word, (626, 68 + 88 * i), team_word)

        team_a_num = -1
        team_b_num = -1

        for player in detail['player_details']:
            player_id = player['openid']
            hero_id = player['championId']
            is_mvp = True if player['battleHonour']['isMvp'] else False
            is_svp = True if player['battleHonour']['isSvp'] else False
            K = player['championsKilled']
            D = player['numDeaths']
            A = player['assists']

            hero_img = await wg_api.get_resource('champions', hero_id)
            hero_img = hero_img.convert('RGBA')
            hero_pic = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
            hero_pic.paste(hero_img, (13, 13), hero_img)

            if player['teamId'] == '100':
                hero_pic.paste(team_a_icon, (0, 0), team_a_icon)
                team_a_num += 1
            else:
                hero_pic.paste(team_b_icon, (0, 0), team_b_icon)
                team_b_num += 1

            hero_draw = ImageDraw.Draw(hero_pic)
            hero_draw.text((50, 77), f'{K}/{D}/{A}', 'white', cf(18), 'mm')

            if is_svp:
                hero_pic.paste(svp, (48, 15), svp)
            elif is_mvp:
                hero_pic.paste(mvp, (48, 15), mvp)

            if _id == player_id:
                me_icon = hero_pic

            if player['teamId'] == '100':
                battle_bg.paste(
                    hero_pic, (178 + 88 * team_a_num, 54), hero_pic
                )
            else:
                battle_bg.paste(
                    hero_pic, (178 + 88 * team_b_num, 145), hero_pic
                )

        me_icon = me_icon.resize((120, 120))
        battle_bg.paste(me_icon, (56, 51), me_icon)
        battle_draw = ImageDraw.Draw(battle_bg)
        battle_draw.text((118, 178), result_str, result_color, cf(25), 'mm')
        battle_draw.text((118, 222), formatted_date, S, cf(16), 'mm')

        img.paste(battle_bg, (0, 500 + index * 242), battle_bg)

    '''FOOTER'''
    footer = Image.open(TEXT_PATH / 'footer.png')
    img.paste(footer, (0, h - 55), footer)

    return await convert_img(img)
