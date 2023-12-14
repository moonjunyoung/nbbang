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

    def add(self, user_id):
        user: User = self.user_repository.ReadByID(user_id).run()
        meeting = Meeting.create_template(user_id)
        meeting.load_user_deposit_information(user)
        self.meeting_repository.Create(meeting).run()
        return meeting

    def edit(
        self,
        id,
        user_id,
        name=None,
        date=None,
        kakao_depoist_id=None,
        bank=None,
        account_number=None,
    ):
        meeting: Meeting = self.meeting_repository.ReadByID(id).run()
        meeting.is_user_of_meeting(user_id)
        if name and date:
            meeting.update_information(name, date)
        elif kakao_depoist_id:
            meeting.update_kakao_deposit_information(kakao_depoist_id)
        elif bank and account_number:
            meeting.update_toss_deposit_information(bank, account_number)
        self.meeting_repository.Update(meeting).run()

    def remove(self, id, user_id):
        meeting: Meeting = self.meeting_repository.ReadByID(id).run()
        meeting.is_user_of_meeting(user_id)
        self.meeting_repository.Delete(meeting).run()
        self.member_repository.DeleteByMeetingID(meeting.id).run()
        self.payment_repository.DeleteByMeetingID(meeting.id).run()

    def read(self, id, user_id):
        meeting: Meeting = self.meeting_repository.ReadByID(id).run()
        meeting.is_user_of_meeting(user_id)
        meeting.create_share_link()
        return meeting

    def read_meetings(self, user_id):
        meetings = self.meeting_repository.ReadByUserID(user_id).run()
        return meetings
