from datetime import timedelta, date ,datetime
import time



def add_date():
    today = date.today()
    end = today + timedelta(days=365)
    return [str(end), str(today)]

def add_custom_date(days):
    """Add custom number of days to current date"""
    today = date.today()
    end = today + timedelta(days=days)
    return [str(end), str(today)]


def check_expi(saved_date):
	today = date.today()
	pattern = '%Y-%m-%d'
	epcho = int(time.mktime(time.strptime(str(today), pattern)))
	
	# Convert saved_date to timestamp if it's a string
	if isinstance(saved_date, str):
		saved_timestamp = int(time.mktime(time.strptime(saved_date, pattern)))
	else:
		saved_timestamp = saved_date
	
	then = saved_timestamp - epcho
	print(then)
	if then > 0:
		return True
	else:
		return False