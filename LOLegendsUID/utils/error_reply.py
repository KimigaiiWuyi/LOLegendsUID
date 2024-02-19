from typing import Union

UID_HINT = '[lol] 你还没有绑定UID，请先使用[lol绑定]命令进行绑定'
CK_HINT = '[lol] 你还没有添加可用CK，请先使用[lol添加ck]命令进行绑定'

error_dict = {
    -51: UID_HINT,
    -511: CK_HINT,
    8000102: '8000102 - auth check failed!\n该CK失效或不正确, 请检查错误CK!',
    8000004: '未找到相关召唤师！\n请确认召唤师名是否完整, 以及Wegame设置是否允许他人搜索！',
}


def get_error(retcode: Union[int, str]) -> str:
    return error_dict.get(
        int(retcode),
        f'未知错误, 错误码为{retcode}, 可能由于未开启Wegame召唤师搜索!',
    )
