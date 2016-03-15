from django.conf import settings as settings_file


#Site_vars: return settings strings for distinct the project
#You can add variables in ticketator/settings.py and include
#thus in the dict key, to be rendered in each function you need
#Note: remember to import as "from core import views_utils"

# def site_vars():
# 	site_vars_data = {}
# 	site_vars_data['name']=settings_file.SITE_NAME
# 	site_vars_data['version']=settings_file.SITE_VERSION
# 	return site_vars_data

def now():
	obj_now = datetime.now().strftime("%d/%m/%y")
	return obj_now
