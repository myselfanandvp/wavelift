from users.models import User
from products.models import Product,Category,ProductImage
from pprint import pprint
from django.db import connection
from datetime import datetime
from time import sleep

print([ (i[0],i[0]) for i  in Product.objects.select_related('category').values_list("category__name").distinct()])




pprint(connection.queries)