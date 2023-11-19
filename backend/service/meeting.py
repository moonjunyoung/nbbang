from backend.domain.meeting import Meeting
from backend.domain.user import User
from backend.repository.meeting import MeetingRepository
from backend.repository.member import MemberRepository
from backend.repository.payment import PaymentRepository
from backend.repository.user import UserRepository


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
        meeting.set_deposit(user.deposit)
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
            self.meeting_repository.UpdateInFo(meeting).run()

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
        return meeting
