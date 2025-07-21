from users.models import User
from products.models import Product_images
from pprint import pprint
from django.db import connection
from datetime import datetime
from time import sleep

user = User.objects.filter().order_by('-created_at')

print(user)
pprint(connection.queries)