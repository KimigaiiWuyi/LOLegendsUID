from gsuid_core.models import Event

from ..utils.lol_config import majs_config
from ..utils.database.models import LOLUser


async def add_cookie(ev: Event, ck: str):
    await LOLUser.insert_data(ev.user_id, ev.bot_id, cookie=ck)
    # 同步到网页控制台WegameCK文本框, 保证命令添加的CK在后台可见
    if ck:
        majs_config.set_config('wegame_cookie', ck)
    return '添加成功！'
