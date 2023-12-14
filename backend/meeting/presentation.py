from typing import Optional

from fastapi import APIRouter, Header, Request, Response
from pydantic import BaseModel

from backend.base.exceptions import catch_exception
from backend.base.token import Token
from backend.meeting.service import MeetingService

meeting_service = MeetingService()


class MeetingData(BaseModel):
    name: str = None
    date: str = None
    bank: str = None
    account_number: str = None
    kakao_id: str = None


class DepositInformationData(BaseModel):
    bank: Optional[str] = None
    account_number: Optional[str] = None
    kakao_deposit_id: Optional[str] = None


class MeetingPresentation:
    router = APIRouter(prefix="/api/meeting")

    @router.post("", status_code=201)
    async def add(
        request: Request,
        response: Response,
        Authorization=Header(None),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = meeting_service.add(user_id)

            response.headers["Location"] = f"meeting/{meeting.id}"
        except Exception as e:
            catch_exception(e, request)

    @router.get("", status_code=200)
    async def read_meetings(Authorization=Header(None)):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meetings = meeting_service.read_meetings(user_id)
            return meetings
        except Exception as e:
            catch_exception(e)

    @router.get("/{meeting_id}", status_code=200)
    async def read(meeting_id: int, Authorization=Header(None)):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = meeting_service.read(
                id=meeting_id,
                user_id=user_id,
            )
            return meeting
        except Exception as e:
            catch_exception(e)

    @router.put("/{meeting_id}", status_code=200)
    async def edit(
        meeting_id: int, meeting_data: MeetingData, Authorization=Header(None)
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.edit(
                id=meeting_id,
                name=meeting_data.name,
                date=meeting_data.date,
                user_id=user_id,
            )
        except Exception as e:
            catch_exception(e)

    @router.delete("/{meeting_id}", status_code=200)
    async def remove(meeting_id: int, Authorization=Header(None)):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.remove(
                id=meeting_id,
                user_id=user_id,
            )
        except Exception as e:
            catch_exception(e)

    @router.patch("/{meeting_id}/kakao-deposit-id", status_code=200)
    async def edit_kakao_deposit_information(
        meeting_id: int,
        deposit_information_data: DepositInformationData,
        Authorization=Header(None),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.edit(
                id=meeting_id,
                user_id=user_id,
                kakao_deposit_id=deposit_information_data.kakao_deposit_id,
            )
        except Exception as e:
            catch_exception(e)

    @router.patch("/{meeting_id}/bank-account", status_code=200)
    async def edit_toss_deposit_information(
        meeting_id: int,
        deposit_information_data: DepositInformationData,
        Authorization=Header(None),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.edit(
                id=meeting_id,
                user_id=user_id,
                bank=deposit_information_data.bank,
                account_number=deposit_information_data.account_number,
            )
        except Exception as e:
            catch_exception(e)
