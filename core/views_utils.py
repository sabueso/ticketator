from django.conf import settings as settings_file

def now():
	obj_now = datetime.now().strftime("%d/%m/%y")
	return obj_now
