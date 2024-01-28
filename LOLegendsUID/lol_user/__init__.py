from typing import Dict

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.message_models import Button
from gsuid_core.utils.message import send_diff_msg

from .add_ck import add_cookie
from ..utils.error_reply import get_error
from ..utils.database.models import LOLBind
from .search_player import search_player_with_name

lol_user_bind = SV('LOL用户绑定')
lol_add_ck = SV('LOL添加CK', area='DIRECT')


@lol_add_ck.on_prefix(('添加CK', '添加ck'))
async def send_lol_add_ck_msg(bot: Bot, ev: Event):
    ck = ev.text.strip()
    await bot.send(await add_cookie(ev, ck))


@lol_user_bind.on_command(
    (
        '绑定uid',
        '绑定UID',
        '绑定',
        '切换uid',
        '切换UID',
        '切换',
        '删除uid',
        '删除UID',
    ),
    block=True,
)
async def send_lol_bind_uid_msg(bot: Bot, ev: Event):
    uid = ev.text.strip()

    if not uid:
        return await bot.send(
            '该命令需要带上正确的uid!\n如果不知道, 可以使用lol搜索命令查询\n如lol搜索Wuyi'
        )

    await bot.logger.info('[LOL] 开始执行[绑定/解绑用户信息]')
    qid = ev.user_id
    await bot.logger.info('[LOL] [绑定/解绑]UserID: {}'.format(qid))

    if uid and ':' not in uid:
        return await bot.send('你输入了错误的格式!\n请使用lol搜索命令获取正确的UID')

    if '绑定' in ev.command:
        data = await LOLBind.insert_uid(
            qid, ev.bot_id, uid, ev.group_id, is_digit=False
        )
        return await send_diff_msg(
            bot,
            data,
            {
                0: f'[LOL] 绑定UID{uid}成功！',
                -1: f'[LOL] UID{uid}的位数不正确！',
                -2: f'[LOL] UID{uid}已经绑定过了！',
                -3: '[LOL] 你输入了错误的格式!',
            },
        )
    elif '切换' in ev.command:
        retcode = await LOLBind.switch_uid_by_game(qid, ev.bot_id, uid)
        if retcode == 0:
            return await bot.send(f'[LOL] 切换UID{uid}成功！')
        else:
            return await bot.send(f'[LOL] 尚未绑定该UID{uid}')
    else:
        data = await LOLBind.delete_uid(qid, ev.bot_id, uid)
        return await send_diff_msg(
            bot,
            data,
            {
                0: f'[LOL] 删除UID{uid}成功！',
                -1: f'[LOL] 该UID{uid}不在已绑定列表中！',
            },
        )


@lol_user_bind.on_command(('搜索'), block=True)
async def send_lol_search_msg(bot: Bot, ev: Event):
    name = ev.text.strip()
    if not name:
        return await bot.send('必须输入完整的召唤师名称噢！\n例如：lol搜索Wuyi')

    players = await search_player_with_name(name)

    if not players:
        return await bot.send('未找到相关召唤师！\n请确认召唤师名是否完整, 以及Wegame设置是否允许他人搜索！')

    if isinstance(players, Dict):
        buttons = [Button(f'✏️绑定{uid}', f'lol绑定{uid}') for uid in players]
        im = '\n\n'.join(list(players.values()))
    else:
        buttons = None
        im = get_error(players)
    await bot.send_option(im, buttons)
