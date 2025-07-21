from users.models import User
from products.models import Product
from pprint import pprint
from django.db import connection
from datetime import datetime
from time import sleep

product = Product.objects.prefetch_related('images')

for i in product:
    print(i.name,list(i.images.all().values("image")))



pprint(connection.queries)