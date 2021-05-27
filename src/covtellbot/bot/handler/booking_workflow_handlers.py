import os
import threading

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from commons.utils import svg_to_png
from cowin.client import CowinClient
from cowin.model import GenerateOTPResponse, APIResponse, ConfirmOTPResponse, ScheduleAppointmentResponse, \
    GetRecaptchaResponse

INPUT_PHONE, INPUT_OTP, INPUT_CAPTCHA = range(3)

cowin_client = CowinClient()


def handle_start_booking(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Enter your COWIN registered contact number to start booking.")
    action, session_id = query.data.split("/")
    user_data = context.user_data
    user_data['session_id'] = session_id
    return INPUT_PHONE


def handle_input_phone(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    if len(text) >= 10:
        user_data['phone'] = text[-10:]
        update.message.reply_text(f"We got your phone number as {text}. Contacting COWIN to generate OTP...")
        response: GenerateOTPResponse = cowin_client.generate_otp(user_data.get('phone'))
        if response.status == APIResponse.Status.SUCCESS:
            user_data['otp_txnId'] = response.txnId
            update.message.reply_text(f"OTP generated successfully. Please provide the OTP that you'll receive from COWIN shortly.")
        else:
            update.message.reply_text(f"Could not generate new OTP. {response.error_message}")
        return INPUT_OTP
    else:
        update.message.reply_text(f"Invalid phone number {text}")
        return ConversationHandler.END


def handle_input_otp(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    otp = update.message.text
    phone = user_data.get('phone')
    txnId = user_data.get('otp_txnId')
    session_id = user_data.get('session_id')
    update.message.reply_text(f"We're verifying your mobile number {phone} with OTP {otp}. Please wait...")
    response: ConfirmOTPResponse = cowin_client.confirm_otp(otp, txnId)
    if response.status == APIResponse.Status.SUCCESS:
        user_data['cowin_token'] = response.token
        update.message.reply_text("OTP successfully verified. Retrieving captcha...")
        response: GetRecaptchaResponse = cowin_client.get_recaptcha(response.token)
        if response.status == APIResponse.Status.SUCCESS:
            png_image = svg_to_png(response.recaptcha)
            update.message.reply_photo(png_image, caption="Enter the text shown above")
            os.remove(png_image)
            return INPUT_CAPTCHA
        else:
            update.message.reply_text(f"Could not get recaptcha. {response.error_message}")
            return ConversationHandler.END
    else:
        update.message.reply_text(f"Could not verify OTP. {response.error_message}. Please try again!")
        return INPUT_OTP


def handle_input_captcha(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    captcha = update.message.text
    token = user_data.get("cowin_token")
    session_id = user_data.get("session_id")
    response: ScheduleAppointmentResponse = cowin_client.book_first_dose_for_all_beneficiaries(
        session_id, token, captcha
    )
    if response.status == APIResponse.Status.SUCCESS:
        update.message.reply_text(
            "Successfully booked all beneficiaries for first dose of vaccination. Check your COWIN Dashboard for details.")
    else:
        update.message.reply_text(f"Could not book slot. {response.error_message}")
    return ConversationHandler.END


def exit_booking_convo(update: Update, context: CallbackContext) -> None:
    if "booking" in context.user_data:
        del context.user_data["booking"]
    update.message.reply_text("Booking process cancelled!")
    # context.user_data.clear()
    return ConversationHandler.END
