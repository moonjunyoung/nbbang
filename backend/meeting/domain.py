import datetime
import os
import re
import uuid

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv

from backend.base.exceptions import MeetingUserMismatchException
from backend.user.domain import User


class Meeting:
    def __init__(self, id, name, date, user_id, uuid) -> None:
        self.id = id
        self.name = name
        self.date = Date(date).date
        self.user_id = user_id
        self.uuid = uuid

    @staticmethod
    def create_template(user_id):
        return Meeting(
            id=None,
            name="모임명을 설정해주세요",
            date=datetime.date.isoformat(datetime.date.today()),
            user_id=user_id,
            uuid=uuid.uuid4(),
        )

    def load_user_deposit_information(self, user: User):
        self.kakao_deposit_information = user
        self.toss_deposit_information = user

    def update_information(self, name, date):
        self.name = name
        self.date = Date(date).date

    def update_kakao_deposit_information(self, kakao_deposit_id):
        self.kakao_deposit_information = KakaoDepositInformation(kakao_deposit_id)

    def update_toss_deposit_information(self, bank, account_number):
        self.toss_deposit_information = TossDepositInformation(bank, account_number)

    def is_user_of_meeting(self, user_id):
        if not self.user_id == user_id:
            raise MeetingUserMismatchException(user_id, self.id)

    def create_share_link(self):
        self.share_link = f"https://nbbang.shop/share?meeting={self.uuid}"


class Date:
    def __init__(self, date) -> None:
        self.date = date
        if self.date and re.match(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z$", self.date
        ):
            dt = datetime.datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.date = dt.strftime("%Y-%m-%d")


class KakaoDepositInformation:
    def __init__(self, kakao_deposit_id) -> None:
        self.kakao_deposit_id = kakao_deposit_id


load_dotenv()
secret_key = bytes(os.environ.get("ENCRYPT_KEY"), "UTF-8")


def aes_encrypt(plaintext):
    cipher = AES.new(secret_key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    return ciphertext


def aes_decrypt(ciphertext):
    cipher = AES.new(secret_key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode("utf-8")


class TossDepositInformation:
    def __init__(self, bank, account_number) -> None:
        self.bank = bank
        self.account_number = account_number

        if isinstance(self.account_number, str) and isinstance(self.bank, str):
            self._encrypt_account_number_data()
        elif isinstance(self.account_number, bytes) and isinstance(self.bank, bytes):
            self._dncrypt_account_number_data()

    def _encrypt_account_number_data(self):
        self.account_number = aes_encrypt(self.account_number)
        self.bank = aes_encrypt(self.bank)

    def _dncrypt_account_number_data(self):
        self.account_number = aes_decrypt(self.account_number)
        self.bank = aes_decrypt(self.bank)
