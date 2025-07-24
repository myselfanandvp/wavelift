from users.models import User
from products.models import Product,Category,ProductImage
from pprint import pprint
from django.db import connection
from datetime import datetime
from time import sleep

existing_images = Product.objects.prefetch_related("images")





pprint(connection.queries)