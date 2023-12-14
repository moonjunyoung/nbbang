from backend.meeting.repository import MeetingRepository
from backend.user.domain import User
from backend.user.exceptions import IdentifierNotFoundException
from backend.user.repository import UserRepository


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.meeting_repository = MeetingRepository()

    def sign_up(self, identifier, password, name):
        user = User(
            id=None,
            name=name,
            identifier=identifier,
            password=password,
        )
        if self.user_repository.ReadByIdentifier(identifier=user.identifier).run():
            user.identifier_is_not_unique()
        user.password_encryption()
        self.user_repository.Create(user).run()
        return user.id

    def sign_in(self, identifier, password):
        user: User = self.user_repository.ReadByIdentifier(identifier).run()
        if not user:
            raise IdentifierNotFoundException(identifier=identifier)
        user.check_password_match(password)
        return user.id

    def oauth_login(self, name, platform_id, platform):
        user = User(
            id=None,
            name=name,
            platform_id=platform_id,
            platform=platform,
            identifier=None,
            password=None,
        )
        existing_user: User = self.user_repository.ReadByPlatformID(
            platform_id=user.platform_id,
            platform=user.platform,
        ).run()
        if existing_user:
            return existing_user.id
        self.user_repository.Create(user).run()
        return user.id

    def read(self, user_id):
        user: User = self.user_repository.ReadByID(user_id).run()
        del user.password
        return user

    def edit(self, user_id, kakao_deposit_id=None, bank=None, account_number=None):
        user: User = self.user_repository.ReadByID(user_id).run()
        if kakao_deposit_id:
            user.update_kakao_deposit_information(kakao_deposit_id)
        elif bank and account_number:
            user.update_toss_deposit_information(bank, account_number)
        self.user_repository.Update(user).run()
