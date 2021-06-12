from datetime import datetime
import pytz


def aware_utc_now():
    utc_now = datetime.utcnow()
    return utc_now.replace(tzinfo=pytz.utc)
