from backend.domain.meeting import Meeting
from backend.domain.user import User
from backend.repository.connector import MysqlSession
from backend.repository.model import MeetingModel


class MeetingRepository(MysqlSession):
    def create(self, meeting: Meeting):
        meeting_model = MeetingModel(
            id=None,
            name=meeting.name,
            date=meeting.date,
            user_id=meeting.user_id,
        )
        self.session.add(meeting_model)
        self.session.commit()
        meeting.id = meeting_model.id

    def update(self, meeting: Meeting):
        meeting_model = self.session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        meeting_model.name = meeting.name
        meeting_model.date = meeting.date
        self.session.commit()

    def delete(self, meeting: Meeting):
        meeting_model = self.session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        self.session.delete(meeting_model)
        self.session.commit()

    def read_meetings_by_user_id(self, user_id):
        meetings = list()
        meeting_models = self.session.query(MeetingModel).filter(MeetingModel.user_id == user_id).all()
        for meeting_model in meeting_models:
            meeting = Meeting(
                id=meeting_model.id,
                name=meeting_model.name,
                date=meeting_model.date,
                user_id=meeting_model.user_id,
            )
            meetings.append(meeting)
        return meetings
