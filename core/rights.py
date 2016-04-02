from django.contrib.auth.models import User, Group
import models
from django.db.models import Q


def get_rights_for_ticket(user,dept=None):
	#If admin, we define can_edit, if not, we check it via query
	if user.username == 'admin':
		class u_rights_obj(object):
			 def __init__(self):
			 	self.can_edit = True
		return u_rights_obj()
	else:
		#Obtain the user group
		u_group=Group.objects.filter(user=user)
		#Obtain the destination group object
		u_dst_group=models.Department.objects.filter(name=dept)
		#Obtain a registry saved action 
		u_rights=models.Rights.objects.filter(grp_src=u_group,dpt_dst=u_dst_group)
		for i in u_rights:
				u_rights_obj=models.Rights.objects.get(id=i.id)
		return u_rights_obj

def get_depts(user):
	granted_departments=[]
	#Obtain the user group
	u_group=Group.objects.filter(user=user)
	u_rights=models.Rights.objects.filter(grp_src=u_group)
	#Now iterate over the groups, obtain the  "can_view" groups
	for dept in u_rights:
		if dept.can_view == True:
			granted_departments.append(dept.dpt_dst_id)
	#And now, make a Q query with the "OR" operator, to be used as argument for filter in views_ticket
	#Magic sponsored by stackoverflow => http://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
	queries = [Q(assigned_department_id=value) for value in granted_departments]
	query = queries.pop()
	for item in queries:
		query |= item
	#End of magic
	return query
