from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.name} borrowed {self.book.title}"    

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User )
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Notification(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.member.name}"
    
def borrow_book(request, book_id):
    if request.method == 'POST':
        member = request.user.member
        book = Book.objects.get(id=book_id)
    Notification.objects.create(member=member, message=f"You have borrowed '{book.title}'.")

def return_book(request, borrowing_id):
    borrowing = Borrowing.objects.get(id=borrowing_id)
    Notification.objects.create(member=borrowing.member, message=f"You have returned '{borrowing.book.title}'.")

