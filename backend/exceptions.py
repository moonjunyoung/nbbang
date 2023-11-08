import traceback

from fastapi import HTTPException


def catch_exception(exce):
    if issubclass(exce.__class__, CustomException):
        print(f"=== A custom error occurred. : {exce} ===")
        raise HTTPException(status_code=exce.status_code, detail=exce.detail)
    print(f"=== An unexpected error occurred. : {exce} ===")
    print(f"=== detail : {traceback.format_exc()} ===")
    raise HTTPException(
        status_code=500,
        detail="An internal server error occurred. If the problem persists, please contact our support team.",
    )


class CustomException(Exception):
    status_code = ""
    detail = ""


class InvalidTokenException(CustomException):
    def __init__(self) -> None:
        super().__init__(f"invalid authorization token.")

    status_code = 401
    detail = "invalid authorization token."


class MissingTokenException(CustomException):
    def __init__(self) -> None:
        super().__init__(f"authorization token is missing.")

    status_code = 401
    detail = "authorization token is missing."


class MeetingUserMismatchException(CustomException):
    def __init__(self, user_id, meeting_id) -> None:
        super().__init__(f"this user:{user_id} does not own the meeting:{meeting_id}.")

    status_code = 403
    detail = "this user does not own the meeting."


class LeaderAlreadyException(CustomException):
    def __init__(self) -> None:
        super().__init__(f"this meeting already has a leader.")

    status_code = 409
    detail = "this meeting already has a leader."


class PaymentInMemberDeleteExcption(CustomException):
    def __init__(self) -> None:
        super().__init__(f"member included in payment cannot be deleted.")

    status_code = 409
    detail = "it is not possible to delete the member you want to delete because it is included in the payment."


class MemberIsLeaderDeleteExcption(CustomException):
    def __init__(self) -> None:
        super().__init__(f"the leader member cannot be deleted.")

    status_code = 409
    detail = "the leader member cannot be deleted."


class SharePageNotMeetingExcption(CustomException):
    def __init__(self) -> None:
        super().__init__(f"That shared page has been deleted or is invalid")

    status_code = 404
    detail = "That shared page has been deleted or is invalid"
