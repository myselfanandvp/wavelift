from users.models import User
from pprint import pprint
from django.db import connection

u = User.objects.filter(username__isnull=True).first()

pprint(connection.queries)