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
        if user_data is None:
            # email not exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # tell user pass is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        """
        Registers user using email and passsword.
        The password comes in hashed as sha_512
        :param email: udrtd email
        :param password: sha-512 hashed password
        :return: True if registered
        """
        user_data = Database.find_one("users", {"email": email})

        if user_data is not None:
            # Tell the user this already exists
            raise UserErrors.UserAlreadyRegisteredError("The e -mail you used already exists.")
        if not Utils.email_is_valid(email):
            # Tell user this email is not constructed right
            raise UserErrors.InvalidEmailError("The e-mail dos not have the right format")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }