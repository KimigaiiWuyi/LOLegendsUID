import asyncio
import threading

from gsuid_core.logger import logger

from ..utils.lol_api import wg_api


async def all_start():
    try:
        await wg_api.get_hero_list()
    except Exception as e:
        logger.exception(e)


threading.Thread(target=lambda: asyncio.run(all_start()), daemon=True).start()
