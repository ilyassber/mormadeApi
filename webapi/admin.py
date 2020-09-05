from django.contrib import admin
from . models.product import product
from . models.tag import tag
from . models.user import user
from . models.token import token
from . models.image import image

admin.site.register(product)
admin.site.register(tag)
admin.site.register(user)
admin.site.register(token)
admin.site.register(image)