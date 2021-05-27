import hashlib
import requests

from commons.constants import cowin_host, generate_otp_api, cowin_request_headers, confirm_otp_api, \
    get_beneficiaries_api, schedule_appointment_api, api_secret, get_recaptcha_api
from commons.utils import get_logger
from cowin.model import GenerateOTPResponse, APIResponse, ConfirmOTPResponse, ScheduleAppointmentResponse, \
    GetRecaptchaResponse

logger = get_logger(__name__)


class CowinClient:

    def authenticated_headers(self, token):
        return {**cowin_request_headers, "Authorization": f"Bearer {token}"}

    def generate_otp(self, mobile) -> GenerateOTPResponse:
        url = generate_otp_api.format(cowin_host)
        response = requests.post(url, json={"mobile": mobile, "secret": api_secret}, headers=cowin_request_headers)
        logger.info(response.text)
        if "OTP Already Sent" in response.text:
            return GenerateOTPResponse(
                status=APIResponse.Status.FAILURE,
                error_message="OTP has already been sent to this mobile number. Use the last received OTP.",
                txnId=None
            )
        else:
            try:
                response_json = response.json()
                if "txnId" in response_json:
                    return GenerateOTPResponse(
                        status=APIResponse.Status.SUCCESS,
                        error_message=None,
                        txnId=response_json.get("txnId")
                    )
            except Exception as e:
                logger.exception(str(e))
            return GenerateOTPResponse(
                status=APIResponse.Status.FAILURE,
                error_message=None,
                txnId=response.text
            )

    def confirm_otp(self, otp, txnId) -> ConfirmOTPResponse:
        url = confirm_otp_api.format(cowin_host)
        response = requests.post(url, json={
            "otp": hashlib.sha256(otp.encode('utf-8')).hexdigest(),
            "txnId": txnId
        }, headers=cowin_request_headers)
        if response.status_code == 200:
            response_json = response.json()
            logger.info(response_json)
            return ConfirmOTPResponse(
                status=APIResponse.Status.SUCCESS,
                error_message=None,
                token=response_json.get("token")
            )
        else:
            return ConfirmOTPResponse(
                status=APIResponse.Status.FAILURE,
                error_message=response.text,
                token=None
            )

    def get_all_beneficiaries(self, token):
        url = get_beneficiaries_api.format(cowin_host)
        response = requests.get(url, headers=self.authenticated_headers(token))
        if response.status_code == 200:
            return response.json().get("beneficiaries")
        else:
            logger.error(f"Could not get beneficiaries. {response.text}")

    def book_first_dose_for_all_beneficiaries(self, session_id, token, captcha):
        payload = {
            "dose": 1,
            "captcha": captcha,
            "session_id": session_id,
            "slot": "FORENOON",
            "beneficiaries": [
                b.get("beneficiary_reference_id") for b in self.get_all_beneficiaries(token)
            ]
        }
        url = schedule_appointment_api.format(cowin_host)
        response = requests.post(url, payload, headers=self.authenticated_headers(token))
        if response == 200:
            response_json = response.json()
            logger.info(f"Appointment booked. Appointment ID: {response_json.get('appointment_id')}")
            return ScheduleAppointmentResponse(
                status=APIResponse.Status.SUCCESS,
                error_message=None,
                appointment_id=response_json.get('appointment_id')
            )
        else:
            return ScheduleAppointmentResponse(
                status=APIResponse.Status.FAILURE,
                error_message=response.text,
                appointment_id=None
            )

    def get_recaptcha(self, token):
        url = get_recaptcha_api.format(cowin_host)
        response = requests.post(url, headers=self.authenticated_headers(token))
        if response.status_code == 200:
            response_json = response.json()
            return GetRecaptchaResponse(
                status=APIResponse.Status.SUCCESS,
                error_message=None,
                recaptcha=response_json.get("captcha")
            )
        else:
            return GetRecaptchaResponse(
                status=APIResponse.Status.FAILURE,
                error_message=response.text,
                recaptcha=None
            )
