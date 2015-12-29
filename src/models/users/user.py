import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent  by the site forms) is valid or not
        Checks that the email exists, ant the the password asscociated is correct
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one("users", {"email": email})  # Pass in sha512 -> pbkdf2_sha512
        print(user_data['password'])
        print(password)
        if user_data is None:
            # email not exist
            raise UserErrors.UserNotExistsError("Your user does not exist."+email)
        if not Utils.check_hashed_password(password, user_data['password']):
            # tell user pass is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True
