from django.contrib import admin
from . models import *
from django.contrib.auth.models import User
from django.forms import Textarea,TextInput
# Register your models here.

admin.site.register(Category)

# class Product(admin.ModelAdmin):
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'20'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
#     }


admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(ProductInventory)
admin.site.register(Profile)
admin.site.register(Comment)

#mix profile info and user info

class ProfileInline(admin.StackedInline):
    model = Profile


#extend the user model

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email', 'phone']
    inlines = [ProfileInline]


admin.site.unregister(User)


admin.site.register(User, UserAdmin)