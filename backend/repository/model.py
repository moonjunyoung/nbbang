from sqlalchemy import Boolean, Column, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    platform = Column(String)

    def __init__(self, id, name, email, platform):
        self.id = id
        self.name = name
        self.email = email
        self.platform = platform


class MeetingModel(Base):
    __tablename__ = "meeting"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    date = Column(String)
    user_id = Column(Integer)
    uuid = Column(String)
    account_number = Column(LargeBinary)
    bank = Column(LargeBinary)

    def __init__(self, id, name, date, user_id, uuid, account_number, bank):
        self.id = id
        self.name = name
        self.date = date
        self.user_id = user_id
        self.uuid = uuid
        self.account_number = account_number
        self.bank = bank


class MemberModel(Base):
    __tablename__ = "member"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    leader = Column(Boolean)
    meeting_id = Column(Integer)

    def __init__(self, id, name, leader, meeting_id):
        self.id = id
        self.name = name
        self.leader = leader
        self.meeting_id = meeting_id


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
