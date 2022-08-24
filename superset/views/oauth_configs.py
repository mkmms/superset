from typing import Any, Dict

from flask_appbuilder import CompactCRUDMixin
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _
from wtforms.validators import DataRequired

from superset.constants import MODEL_VIEW_RW_METHOD_PERMISSION_MAP, RouteMethod
from superset.views.base import SupersetModelView
from superset.models.oauth_config import OAuthConfig

class OAuthConfigModelView(
    SupersetModelView,
    CompactCRUDMixin
):
    datamodel = SQLAInterface(OAuthConfig)
    include_route_methods = RouteMethod.CRUD_SET | {"oauth_config"}
    
    # class_permission_name: str = "OAuthConfig"
    # method_permission_name = MODEL_VIEW_RW_METHOD_PERMISSION_MAP
    
    list_title = _("OAuth Configs")
    show_title = _("Show OAuth Config")
    add_title = _("Add OAuth Config")
    edit_title = _ ("Edit OAuth Config")
    
    list_columns = [
        "name",
        "token_key",
        "client_id",
        "client_secret",
        "api_base_url",
        "access_token_url",
        "authorize_url"
    ]
    
    edit_columns = list_columns
    
    add_columns = list_columns
    
    label_columns = {
        "name": _("OAuth Config Name"),
        "token_key": _("OAuth Config Token Key"),
        "client_id": _("OAuth Config ClientID"),
        "client_secret": _("OAuth Config Client Secret"),
        "api_base_url": _("OAuth Config API Base URL"),
        "access_token_url": _("OAuth Config Access Token"),
        "authorize_url": _("OAuth Config Authorize URL"),
    }
    
    validators_columns = {"name": [DataRequired()]}