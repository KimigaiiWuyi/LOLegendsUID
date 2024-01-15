from typing import Optional

from sqlmodel import Field
from gsuid_core.utils.database.base_models import Bind, User
from gsuid_core.webconsole.mount_app import PageSchema, GsAdminModel, site


class LOLBind(Bind, table=True):
    uid: Optional[str] = Field(default=None, title='LOLUID')


class LOLUser(User, table=True):
    uid: Optional[str] = Field(default=None, title='LOLUID')


@site.register_admin
class LOLBindadmin(GsAdminModel):
    pk_name = 'id'
    page_schema = PageSchema(
        label='LOL绑定管理',
        icon='fa fa-users',
    )  # type: ignore

    # 配置管理模型
    model = LOLBind


@site.register_admin
class LOLUseradmin(GsAdminModel):
    pk_name = 'id'
    page_schema = PageSchema(
        label='LOL用户管理',
        icon='fa fa-users',
    )  # type: ignore

    # 配置管理模型
    model = LOLUser
