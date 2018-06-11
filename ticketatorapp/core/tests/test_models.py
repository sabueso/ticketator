# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import (
    UserType, User, Company, Queue, Rights, State, Priority, Ticket, Attachment, Comments,
    Microtasks, Logs
)

# Run tests: docker-compose exec backend ./ticketatorapp/manage.py test core.tests
# Coverage: docker-compose exec backend coverage run --source='.' ticketatorapp/manage.py test core.tests

class MainMethods(TestCase):
    def create_user_type(self):
        return UserType.objects.create(status='test status')

    def create_user(self, username):
        return User.objects.create(username=username, first_name='Test', last_name='User',
                                        # password_first='ticketator', password_check='ticketator',
                                        email='test@ticketator.com', is_superuser=True)

    def create_company(self):
        return Company.objects.create(name='Test Company')

    def create_queue(self):
        return Queue.objects.create(name='Test Queue', shortcode='TQ',
                                    company_rel=self.create_company())

    def create_rights(self):
        return Rights.objects.create(queue_dst=self.create_queue(), can_view=True, can_comment=True)

    def create_state(self):
        return State.objects.create(name='Open', color='00FF00')

    def create_priority(self):
        return Priority.objects.create(name='High')

    def create_ticket(self):
        return Ticket.objects.create(create_user=self.create_user('testuser'),
                                     subject='Ticket subject', body='Ticket body',
                                     assigned_user=self.create_user('testuser2'),
                                     assigned_queue=self.create_queue(),
                                     assigned_company=self.create_company(),
                                     assigned_state=self.create_state(),
                                     assigned_prio=self.create_priority(), labels='test,ticket, hi')

    def create_attachment(self):
        return Attachment.objects.create(ticket_rel=self.create_ticket(),
                                         file_name=SimpleUploadedFile('dodo.png', b'Test file'))

    def create_comments(self):
        return Comments.objects.create(ticket_rel=self.create_ticket(),
                                      user_rel=self.create_user('testuser3'), comment='Lorem Ipsum')

    def create_microtasks(self):
        return Microtasks.objects.create(ticket_rel=self.create_ticket(), subject='Microtask Test',
                                         body='Microtask test body',
                                         assigned_state=self.create_state())

    def create_logs(self):
        return Logs.objects.create(log_ticket=self.create_ticket(),
                                   log_user=self.create_user('testuser4'), log_action='Test log')


class UserTypeTest(MainMethods):
    def test_user_creation(self):
        user_type = self.create_user_type()
        self.assertTrue(isinstance(user_type, UserType))
        self.assertEqual(user_type.__unicode__(), user_type.status)


class UserTest(MainMethods):
    def test_user_creation(self):
        user = self.create_user('testuser')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.email, 'test@ticketator.com')
        self.assertTrue(user.is_superuser)


class CompanyTest(MainMethods):
    def test_company_creation(self):
        company = self.create_company()
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.__unicode__(), company.name)


class QueueTest(MainMethods):
    def test_queue_creation(self):
        queue = self.create_queue()
        self.assertTrue(isinstance(queue, Queue))
        self.assertEqual(queue.__unicode__(), queue.name)
        self.assertNotEqual(queue.shortcode, 'AZ')


class RightsTest(MainMethods):
    def test_rights_creation(self):
        rights = self.create_rights()
        self.assertTrue(isinstance(rights, Rights))
        self.assertTrue(rights.can_view)
        self.assertFalse(rights.can_edit)


class StateTest(MainMethods):
    def test_state_creation(self):
        state = self.create_state()
        self.assertTrue(isinstance(state, State))
        self.assertEqual(state.__unicode__(), state.name)
        self.assertNotEqual(state.color, 'A801F2')


class PriorityTest(MainMethods):
    def test_priority_creation(self):
        priority = self.create_priority()
        self.assertTrue(isinstance(priority, Priority))
        self.assertEqual(priority.__unicode__(), priority.name)


class TicketTest(MainMethods):
    def test_ticket_creation(self):
        ticket = self.create_ticket()
        self.assertTrue(isinstance(ticket, Ticket))
        self.assertEqual(ticket.__str__(), str(ticket.id))
        self.assertNotEqual(ticket.subject, 'Test subject')
        self.assertEqual(ticket.str_assigned_user_name(), 'Test User')
        self.assertEqual(ticket.str_creator_user_name(), 'Test User')
        self.assertEqual(ticket.get_label_list(), ['test', 'ticket', 'hi'])


class AttachmentTest(MainMethods):
    def test_attachment_creation(self):
        attachment = self.create_attachment()
        self.assertTrue(isinstance(attachment, Attachment))
        self.assertEqual(attachment.file_name.path, '/code/media/ticket_files/1/dodo.png')


class CommentsTest(MainMethods):
    def test_comments_creation(self):
        comments = self.create_comments()
        self.assertTrue(isinstance(comments, Comments))
        self.assertEqual(comments.comment, 'Lorem Ipsum')


class MicrotasksTest(MainMethods):
    def test_microtasks_creation(self):
        microtasks = self.create_microtasks()
        self.assertTrue(isinstance(microtasks, Microtasks))
        self.assertEqual(microtasks.subject, 'Microtask Test')


class LogsTest(MainMethods):
    def test_logs_creation(self):
        logs = self.create_logs()
        self.assertTrue(isinstance(logs, Logs))
        self.assertEqual(logs.log_action, 'Test log')
