from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True)
    identifier = Column(String)
    password = Column(String)

    def __init__(self, id, identifier, password):
        self.id = id
        self.identifier = identifier
        self.password = password


class MeetingModel(Base):
    __tablename__ = "meeting"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    date = Column(String)
    user_id = Column(Integer)

    def __init__(self, id, name, date, user_id):
        self.id = id
        self.name = name
        self.date = date
        self.user_id = user_id


class MemberModel(Base):
    __tablename__ = "member"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    meeting_id = Column(Integer)

    def __init__(self, id, name, meeting_id):
        self.id = id
        self.name = name
        self.meeting_id = meeting_id


class LeaderModel(Base):
    __tablename__ = "leader"
    id = Column("id", Integer, primary_key=True)
    meeting_id = Column(Integer)
    member_id = Column(Integer)

    def __init__(self, id, meeting_id, member_id):
        self.id = id
        self.meeting_id = meeting_id
        self.member_id = member_id


class PaymentModel(Base):
    __tablename__ = "payment"
    id = Column("id", Integer, primary_key=True)
    place = Column(String)
    price = Column(Integer)
    pay_member_id = Column(Integer)
    attend_member_ids = Column(String)
    meeting_id = Column(Integer)

    def __init__(self, id, place, price, pay_member_id, attend_member_ids, meeting_id):
        self.id = id
        self.place = place
        self.price = price
        self.pay_member_id = pay_member_id
        self.attend_member_ids = attend_member_ids
        self.meeting_id = meeting_id
