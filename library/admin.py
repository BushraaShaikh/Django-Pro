from django.contrib import admin
# Register your models here.
from .models import Book, Author, Member, Borrowing

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Member)
admin.site.register(Borrowing)