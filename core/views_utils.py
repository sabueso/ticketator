import datetime


def now():
    obj_now = datetime.now().strftime("%d/%m/%y")
    return obj_now
