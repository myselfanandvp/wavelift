from users.models import User
from products.models import Product,Category,ProductImage
from pprint import pprint
from django.db import connection
from datetime import datetime
from time import sleep

greater_price = Product.objects.filter(price__gte=5)
lesser_price = Product.objects.filter(price__lte=1000)

print(lesser_price)





pprint(connection.queries)