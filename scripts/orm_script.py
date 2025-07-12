from users.models import User
from pprint import pprint
from django.db import connection

u = User.objects.all()

print(u)

pprint(connection.queries)