from superset.security import SupersetSecurityManager
from flask_appbuilder.security.sqla.models import User
from werkzeug.security import generate_password_hash
from sqlalchemy import (
    Column, 
    BigInteger,
    String
)
import logging
log = logging.getLogger(__name__)
def get_user_role(role, user_type):
    logging.debug("===========================")
    logging.debug("====== Role:  %s", role)
    logging.debug("====== UserType:  %s", user_type)
    logging.debug("===========================")
    return "Admin"


class CustomUser(User):
    __tablename__ = "ab_user"
    travel_id = Column(BigInteger())
    travel_name = Column(String(255))
    user_type = Column(String(64))
    user_role = Column(String(64))

class CustomSecurityManager(SupersetSecurityManager):
    def __init__(self, appbuilder):
        super(SupersetSecurityManager, self).__init__(appbuilder)

    def oauth_user_info(self, provider, response=None):
        #for ticketsimply
        # if re.match("\.ticketsimply", provider):
        if provider == "ticketsimply":
            me = self.appbuilder.sm.oauth_remotes[provider].get("api/auth/me.json")
            data = me.json()
            return {
                "travel_id": data.get("travel_id", ""),
                "travel_name": data.get("travel_name", ""),
                "username": data.get("username", ""),
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "email": data.get("email", ""),
                "role_keys": get_user_role(data.get("role"), data.get("user_type")),
                "user_type": data.get("user_type"),
                "user_role": data.get("role")
            }

    def auth_user_oauth(self, userinfo):
        """
        Method for authenticating user with OAuth.

        :userinfo: dict with user information
                   (keys are the same as User model columns)
        """
        # extract the username from `userinfo`
        if "username" in userinfo:
            username = userinfo["username"]
        elif "email" in userinfo:
            username = userinfo["email"]
        else:
            log.error(
                "OAUTH userinfo does not have username or email {0}".format(userinfo)
            )
            return None

        # If username is empty, go away
        if (username is None) or username == "":
            return None

        # Search the DB for this user
        user = self.find_user(username=username)

        # If user is not active, go away
        if user and (not user.is_active):
            return None

        # If user is not registered, and not self-registration, go away
        if (not user) and (not self.auth_user_registration):
            return None

        # Sync the user's roles
        if user and self.auth_roles_sync_at_login:
            user.roles = self._oauth_calculate_user_roles(userinfo)
            log.debug(
                "Calculated new roles for user='{0}' as: {1}".format(
                    username, user.roles
                )
            )

        # If the user is new, register them
        if (not user) and self.auth_user_registration:
            user = self.add_user(
                travel_id=userinfo.get("travel_id", ""),
                travel_name=userinfo.get("travel_name", ""),
                username=username,
                first_name=userinfo.get("first_name", ""),
                last_name=userinfo.get("last_name", ""),
                email=userinfo.get("email", "") or f"{username}@email.notfound",
                role=self._oauth_calculate_user_roles(userinfo),
                user_type=userinfo.get("user_type", ""),
                user_role=userinfo.get("user_role", "")
            )
            log.debug("New user registered: {0}".format(user))

            # If user registration failed, go away
            if not user:
                log.error("Error creating a new OAuth user {0}".format(username))
                return None

        # LOGIN SUCCESS (only if user is now registered)
        if user:
            self.update_user_auth_stat(user)
            return user
        else:
            return None

    def add_user(
        self,
        travel_id,
        travel_name,
        username,
        first_name,
        last_name,
        email,
        role,
        user_type,
        user_role,
        password="",
        hashed_password="",
    ):
        try:
            user = CustomUser()
            user.travel_id = travel_id
            user.travel_name = travel_name
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.active = True
            user.roles = role if isinstance(role, list) else [role]
            user.user_type = user_type
            user.user_role = user_role

            if hashed_password:
                user.password = hashed_password
            else:
                user.password = generate_password_hash(password)
            self.get_session.add(user)
            self.get_session.commit()
            logging.info("User logged in!")
            return user
        except Exception as e:
            logging.error("Error %s", e)
            self.get_session.rollback()
            return False