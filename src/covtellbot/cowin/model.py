from dataclasses import dataclass
from enum import Enum
from typing import Union


@dataclass()
class APIResponse:
    class Status(Enum):
        SUCCESS = 1
        FAILURE = 2
    status: Status
    error_message: Union[str, None]


@dataclass
class GenerateOTPResponse(APIResponse):
    txnId: Union[str, None]


@dataclass
class ConfirmOTPResponse(APIResponse):
    token: Union[str, None]


@dataclass
class ScheduleAppointmentResponse(APIResponse):
    appointment_id: Union[str, None]


@dataclass
class GetRecaptchaResponse(APIResponse):
    recaptcha: Union[str, None]
