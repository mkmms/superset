from superset.security import SupersetSecurityManager
import logging
logging.debug("====================================")
def get_user_role(role, user_type):
    logging.debug("===========================")
    logging.debug("====== Role:  %s", role)
    logging.debug("====== UserType:  %s", user_type)
    logging.debug("===========================")
    return "Admin"


class CustomSecurityManager(SupersetSecurityManager):
    logging.debug("====================================")
    def __init__(self, appbuilder):
        super(SupersetSecurityManager, self).__init__(appbuilder)

    def oauth_user_info(self, provider, response=None):
        logging.debug("===================================")
        #for ticketsimply
        if provider == "ticketsimply":
            me = self.appbuilder.sm.oauth_remotes[provider].get("api/auth/me.json")
            data = me.json()
            logging.debug("=====================data: %s", data)
            return {
                "username": data.get("username", ""),
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "email": data.get("email", ""),
                "role_keys": get_user_role(data.get("role"), data.get("user_type")),
                "user_type": data.get("user_type")
            }


logging.debug("====================================")