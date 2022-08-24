from typing import Any, Dict

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String

from superset.models.helpers import AuditMixinNullable

class OAuthConfig(Model, AuditMixinNullable):
    __tablename__ = "oauth_configs"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique = True, nullable = False)
    token_key = Column(String(256), nullable = False)
    client_id = Column(String(256), nullable = False)
    client_secret = Column(String(256), nullable = False)
    api_base_url = Column(String(256), nullable = False)
    access_token_url = Column(String(256), nullable = False)
    authorize_url = Column(String(256), nullable = False)
    
    @property
    def data(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "token_key": self.token_key,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "api_base_url": self.api_base_url,
            "access_token_url": self.access_token_url,
            "authorize_url": self.authorize_url
        }

    def __repr__(self) -> str:
        return self.name