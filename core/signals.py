from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from core.models import Microtasks, Ticket


@receiver(post_save, sender=Microtasks)
def update_percentage_average_post_save(sender, instance, **kwargs):
    ticket_id = instance.ticket_rel
    av_percentage = Microtasks.objects.filter(ticket_rel=ticket_id).aggregate(Avg('percentage'))
    av_percentage = av_percentage['percentage__avg']
    ticket_to_update = Ticket.objects.get(id=ticket_id.id)
    ticket_to_update.percentage = av_percentage
    ticket_to_update.save()


@receiver(post_delete, sender=Microtasks)
def update_percentage_average_post_delete(sender, instance, **kwargs):
    ticket_id = instance.ticket_rel
    if Microtasks.objects.filter(ticket_rel=ticket_id):
        av_percentage = Microtasks.objects.filter(ticket_rel=ticket_id).aggregate(Avg('percentage'))
        av_percentage = av_percentage['percentage__avg']
        ticket_to_update = Ticket.objects.get(id=ticket_id.id)
        ticket_to_update.percentage = av_percentage
        ticket_to_update.save()
    else:
        pass


@receiver(post_save, sender=Ticket)
def cent_percent_on_close(sender, instance, **kwargs):
    ticket = instance
    if ticket.assigned_state.id == 3 and ticket.percentage != 100:
        ticket.percentage = int(100)
        ticket.save()
