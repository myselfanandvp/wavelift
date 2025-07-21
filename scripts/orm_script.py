from users.models import User
from products.models import Product_images
from pprint import pprint
from django.db import connection
from datetime import datetime
from time import sleep

user = User.objects.all().values('email','phone_number','is_active','username','id')

print(user)
pprint(connection.queries)