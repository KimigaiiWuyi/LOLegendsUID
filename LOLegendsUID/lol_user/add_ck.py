from gsuid_core.models import Event

from ..utils.database.models import LOLUser


async def add_cookie(ev: Event, ck: str):
    await LOLUser.insert_data(ev.user_id, ev.bot_id, cookie=ck)
    return '添加成功！'
