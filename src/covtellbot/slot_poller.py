import time
import datetime
import requests
from typing import Dict

from bot.service.notifications_service import send_notifications
from commons.constants import MIN_AGE, MIN_CAPACITY, districts, cowin_host, calender_api, cowin_request_headers, \
    DISTRICT_ITERATION_INTERVAL_SECONDS, DISTRICT_SKIP_INTERVAL, COMPLETE_ITERATION_INTERVAL_SECONDS, \
    calender_api_public
from commons.utils import get_logger

logger = get_logger(__name__)

# stores last fetched available slots for a session_id
slot_cache: Dict[str, int] = {}
# stores skip interval for district id
district_cache: Dict[str, int] = {}


def check_slots_in_response(response):
    found_new_free_slots = False
    centers = response.get("centers")
    for center in centers:
        for session in center.get('sessions'):
            session_id = session.get('session_id')
            available_capacity = session.get('available_capacity')
            min_age_limit = session.get('min_age_limit')
            date = session.get('date')
            if min_age_limit == MIN_AGE and MIN_CAPACITY <= available_capacity != slot_cache.get(session_id, -1):
                slot_cache[session_id] = available_capacity
                message = f"**District: {center.get('district_name')}**\n {session.get('available_capacity')} slots " \
                    f"available at {center.get('name')} on {date} for {MIN_AGE}+\n"\
                    f"Address: {center.get('address')}, {center.get('state_name')}-{center.get('pincode')}"
                logger.info(message)
                send_notifications(center, message, session_id)
                found_new_free_slots = True
    return found_new_free_slots


def start_polling():
    logger.info("Starting COWIN Slot poller")
    while True:
        for district_id, district_name in districts.items():
            update_district_cache = True
            if district_cache.get(district_id, 0) != 0:
                district_cache[district_id] -= 1
                continue
            curr_date = datetime.date.today().strftime("%d-%m-%Y")
            url = calender_api.format(cowin_host, str(district_id), curr_date)
            logger.debug(f"url: {url}")
            response = requests.get(url, headers=cowin_request_headers)
            try:
                response_json = response.json()
            except Exception as e:
                # Fallback to public API if realtime API failed for the district
                logger.exception(f"Failed polling COWIN Realtime API at {datetime.datetime.utcnow()} UTC")
                url = calender_api_public.format(cowin_host, str(district_id), curr_date)
                response = requests.get(url, headers=cowin_request_headers)
                try:
                    response_json = response.json()
                except Exception:
                    logger.exception(f"Failed polling COWIN Public API at {datetime.datetime.utcnow()} UTC. Skipping district.")
                    time.sleep(DISTRICT_ITERATION_INTERVAL_SECONDS)
                    continue
                update_district_cache = False
            logger.debug(response.text)
            try:
                if check_slots_in_response(response_json) and update_district_cache:
                    district_cache[district_id] = DISTRICT_SKIP_INTERVAL
            except Exception as e:
                district_cache[district_id] = True
                logger.exception(f"Exception occurred: {str(e)}")
            finally:
                time.sleep(DISTRICT_ITERATION_INTERVAL_SECONDS)
        time.sleep(COMPLETE_ITERATION_INTERVAL_SECONDS)
