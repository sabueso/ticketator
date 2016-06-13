from django.contrib.auth.models import User, Group
import models
from django.db.models import Q


#Check the rights for user =>  ticket or for user =>  queue to bind this in actions
def get_rights_for_ticket(user, queue=None, ticket_id=None):
	#If admin, we define can_edit, if not, we check it via query
	class u_rights_obj(object):
		def __init__(self):
			#Super-admin benefits :)
			if user.username == 'admin':
				self.can_edit = True
				self.can_view = True
				self.can_create = True
				self.can_delete = True
				self.can_comment = True
			else:
				#if ticket_id is given, try to obtain ticket perms
				if ticket_id:
					u_group=Group.objects.filter(user=user)
					u_dst_group=models.Ticket.objects.get(id=ticket_id).assigned_queue
					r_obj=models.Rights.objects.get(grp_src=u_group,queue_dst=u_dst_group)
					#Set the models propertys
					self.can_edit = r_obj.can_edit
					self.can_view = r_obj.can_view
					self.can_create = r_obj.can_create
					self.can_delete = r_obj.can_delete
					self.can_comment = r_obj.can_comment
				else:
					#Obtain the user group
					u_group=Group.objects.filter(user=user)
					#Obtain the destination group object
					if queue == None:
						u_dst_group = None
					else:
						u_dst_group = models.Queue.objects.filter(name=queue)
					#Obtain a registry saved action 
					#If we dont find the group, we assign queue_dst to None
					#to see if global rule is created
					try:
						r_obj = models.Rights.objects.get(grp_src=u_group,queue_dst=u_dst_group)
					except:
						r_obj = models.Rights.objects.get(grp_src=u_group,queue_dst=None)
					#Set the models propertys
					self.can_edit = r_obj.can_edit
					self.can_view = r_obj.can_view
					self.can_create = r_obj.can_create
					self.can_delete = r_obj.can_delete
					self.can_comment = r_obj.can_comment
	return u_rights_obj()

#queues to be listed in the "/tickets" section
def get_queues(user):
	granted_queues=[]
	#Obtain the user group
	u_group=Group.objects.filter(user=user)
	u_rights=models.Rights.objects.filter(grp_src=u_group)
	#Now iterate over the groups, obtain the  "can_view" groups
	for queue in u_rights:
		if queue.can_view == True:
			granted_queues.append(queue.queue_dst_id)
	#And now, make a Q query with the "OR" operator, to be used as argument for filter in views_ticket
	#Magic sponsored by stackoverflow => http://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
	queries = [Q(assigned_queue_id=value) for value in granted_queues]
	query = queries.pop()
	for item in queries:
		query |= item
	#End of magic
	return query
