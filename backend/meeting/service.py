from backend.deposit.domain import Deposit
from backend.meeting.domain import Meeting
from backend.meeting.repository import MeetingRepository
from backend.member.repository import MemberRepository
from backend.payment.repository import PaymentRepository
from backend.user.domain import User
from backend.user.repository import UserRepository


class MeetingService:
    def __init__(self) -> None:
        self.meeting_repository = MeetingRepository()
        self.member_repository = MemberRepository()
        self.payment_repository = PaymentRepository()
        self.user_repository = UserRepository()

    def create(self, user_id):
        user: User = self.user_repository.ReadByID(user_id).run()
        meeting = Meeting(
            id=None,
            name=None,
            date=None,
            user_id=user.id,
            uuid=None,
        )
        meeting.set_template()
        meeting.set_uuid()
        deposit = Deposit(
            bank=user.deposit.bank,
            account_number=user.deposit.account_number,
            kakao_deposit_id=user.deposit.kakao_deposit_id,
        )
        meeting.set_deposit(deposit)
        self.meeting_repository.Create(meeting).run()
        return meeting

    def update(self, id, name, date, user_id):
        meeting: Meeting = self.meeting_repository.ReadByID(id).run()
        meeting.is_user_of_meeting(user_id)
        meeting = Meeting(
            id=id,
            name=name,
            date=date,
            user_id=None,
            uuid=None,
        )
        if meeting.name and meeting.date:
            self.meeting_repository.Update(meeting).run()

    def delete(self, id, user_id):
        meeting: Meeting = self.meeting_repository.ReadByID(id).run()
        meeting.is_user_of_meeting(user_id)
        self.meeting_repository.Delete(meeting).run()
        self.member_repository.DeleteByMeetingID(meeting.id).run()
        self.payment_repository.DeleteByMeetingID(meeting.id).run()

    def read_by_user_id(self, user_id):
        meetings = self.meeting_repository.ReadByUserID(user_id).run()
        return meetings

    def read(self, id, user_id):
        meeting: Meeting = self.meeting_repository.ReadByID(id).run()
        meeting.is_user_of_meeting(user_id)
        meeting.create_share_link()
        return meeting
