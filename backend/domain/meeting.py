import datetime


class Meeting:
    def __init__(self, id, name, date, user_id) -> None:
        self.id = id
        self.name = name
        self.date = date
        self.user_id = user_id

    def set_template(self):
        self.name = "모임명을 입력해주세요"
        self.date = datetime.date.isoformat(datetime.date.today())