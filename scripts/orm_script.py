from users.models import User
from pprint import pprint
from django.db import connection

u = User.objects.filter(email='anand@gmail.com').first()
u.role='admin'
u.save(update_fields=['role'])
pprint(connection.queries)