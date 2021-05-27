import os

# system constants
DOWNSTREAM_ENABLED = True

# bot constants
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# slot poller constants

MIN_AGE = 18    # min age limit to look for
MIN_CAPACITY = 1    # min available slots to look for

DISTRICT_SKIP_INTERVAL = 1  # how many iterations to wait before checking a district that was found to have new slots
COMPLETE_ITERATION_INTERVAL_SECONDS = 90
DISTRICT_ITERATION_INTERVAL_SECONDS = 1

ANY_PINCODE = "ANY"

# subscription constants
SUBSCRIPTIONS_FILE_PATH = "./subscriptions.json"

# COWIN Constants

api_secret = "U2FsdGVkX1/g+SqSDSRAMAhRjOA4ihfPzicBdLttULWCtxTO7lZSsk6+sRJmL+h53NNSN9qPRgU1hIZAWEFzkA=="
cowin_host = "https://cdn-api.co-vin.in/api/v2/"
calender_api = "{}appointment/sessions/calendarByDistrict?district_id={}&date={}"
calender_api_public = "{}appointment/sessions/public/calendarByDistrict?district_id{}&date={}"
generate_otp_api = "{}auth/public/generateOTP"
confirm_otp_api = "{}auth/public/confirmOTP"
schedule_appointment_api = "{}appointment/schedule"
get_beneficiaries_api = "{}appointment/beneficiaries"
get_recaptcha_api = "{}auth/getRecaptcha"

districts = {
    "141": "Central Delhi",
    "145": "East Delhi",
    "140": "New Delhi",
    "146": "North Delhi",
    "147": "North East Delhi",
    "143": "North West Delhi",
    "148": "Shahdara",
    "149": "South Delhi",
    "144": "South East Delhi",
    "150": "South West Delhi",
    "142": "West Delhi"
}


cowin_request_headers = {
    "authority": "cdn-api.co-vin.in",
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "upgrade-insecure-request": "1",
    "sec-ch-ua":'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="9',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-mod": "navigate"
}