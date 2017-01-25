from django.contrib.auth.models import Group
import models
from django.db.models import Q

'''
Check rights for user:
You can pass a queue, or a ticket_id to retrieve all the rights
defined for the users group
'''


def get_rights_for_ticket(user, queue=None, ticket_id=None):
    # If admin, we define can_edit, if not, we check it via query
    class u_rights_obj(object):
        def __init__(self):
            def q_result(query_result):
                if query_result == "all":
                    self.can_edit = True
                    self.can_view = True
                    self.can_create = True
                    self.can_delete = True
                    self.can_comment = True
                elif not query_result:
                    self.can_edit = False
                    self.can_view = False
                    self.can_create = False
                    self.can_delete = False
                    self.can_comment = False
                else:
                    self.can_edit = r_obj.can_edit
                    self.can_view = r_obj.can_view
                    self.can_create = r_obj.can_create
                    self.can_delete = r_obj.can_delete
                    self.can_comment = r_obj.can_comment
                return self
            # Super-admin benefits :)
            if user.username == 'admin':
                q_result("all")
            else:
                # if ticket_id is given, try to obtain ticket perms
                if ticket_id:
                    u_group = Group.objects.filter(user=user)
                    u_dst_group = models.Ticket.objects.get(id=ticket_id).assigned_queue
                    r_obj = models.Rights.objects.get(grp_src=u_group, queue_dst=u_dst_group)
                    # Set the models propertys
                    q_result(r_obj)
                else:
                    # Obtain the user group
                    u_group = Group.objects.filter(user=user)
                    # Obtain the destination group object
                    if not queue:
                        u_dst_group = None
                    else:
                        u_dst_group = models.Queue.objects.filter(name=queue)
                    # Obtain a registry saved action
                    # If we dont find the group, we assign queue_dst to None
                    # to see if global rule is created
                    # Try to match if an specific rule is created
                    try:
                        r_obj = models.Rights.objects.get(grp_src=u_group, queue_dst=u_dst_group)
                        q_result(r_obj)
                    # Also, try to match if a global rule with no queue is defined
                    except models.Rights.DoesNotExist:
                        try:
                            r_obj = models.Rights.objects.get(grp_src=u_group, queue_dst=None)
                            q_result(r_obj)
                        # And in a last way, ensure user to make nothing
                        # if no query is defined at all
                        except models.Rights.DoesNotExist:
                            q_result(None)

    return u_rights_obj()


'''
get_queues:
Used to get all queues for a particular user, and if needed for a particular
right as can_view or can_create
One action for admin, and another for the rest of the mortals
Options for perm_level are can_view, can_create or cv_cc (both of them)
Remember you can have rights to create a ticket but not for see the queue where you created for...
(at time of creation, we pass the argument cv_cc to achieve all targets for rights)

'''


def get_queues(user, perm_level=None):
    granted_queues = []
    # If admin, we return all queues
    if user.username == 'admin':
        [granted_queues.append(queue.id) for queue in models.Queue.objects.all()]
    else:
        # Obtain the user group => # Obtain the rights for that group
        u_rights = models.Rights.objects.filter(grp_src=Group.objects.filter(
            user=user), enabled=True)
        # Now iterate over the groups, obtain the  "can_view" groups
        # [granted_queues.append(queue.queue_dst_id) for queue in u_rights if
        # queue.can_view == True ]
        if perm_level == 'can_view':
            [granted_queues.append(queue.queue_dst_id) for queue in u_rights if queue.can_view]
        elif perm_level == 'can_create':
            [granted_queues.append(queue.queue_dst_id) for queue in u_rights if queue.can_create]
        elif perm_level == 'cv_cc':
            [granted_queues.append(
                queue.queue_dst_id) for queue in u_rights if queue.can_create or queue.can_view]
    return granted_queues

'''
Designed to interact with Tickets model
Return a Q object for assigned_queue_id, used in list_tickest()
With this object we assure that only granted queus with can_view are listed as
granted_queues in function
'''


def get_queues_as_q_for_ticket_model(user):
    can_view = ''
    #  Return a Q query with the "OR" operator, to be used as argument for
    #  filter in views_ticket
    #  Magic sponsored by stackoverflow =>
    #  http://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
    queries = [Q(assigned_queue_id=value) for value in get_queues(user, 'can_view')]
    if not queries:
        query = {'assigned_queue_id': ''}
    else:
        query = queries.pop()
    for item in queries:
        query |= item
    # End of magic
    return query

'''
Designed to interact with Queues model
Return a Q object to use it in other funcionts, as templatags (proxy model for get_queues)
Used in core_settings_data inside a templatetag function
'''


def get_queues_as_q_for_queue_model(user, perm_level=None):
    queries = [Q(id=value) for value in get_queues(user, perm_level)]
    if not queries:
        query = {'id': ''}
    else:
        query = queries.pop()
    for item in queries:
        query |= item
    # End of magic
    return query


# Return the rights as serial (used?)
def get_queues_as_serial(user):
    dict_pre = {'assigned_queue_id': ','.join(map(str, get_queues(user)))}
    params = {key: value for key, value in dict_pre.iteritems() if value}
    return params
