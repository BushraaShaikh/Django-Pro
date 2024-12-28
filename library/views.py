from django.shortcuts import render

# Create your views here.
from .models import Book, Author, Member

def home(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'library/home.html', {'books': books})
'''def home(request):
    books = Book.objects.all()
    return render(request, 'library/home.html', {'books': books})'''

def authors(request):
    authors = Author.objects.all()
    return render(request, 'library/authors.html', {'authors': authors})

def members(request):
    members = Member.objects.all()
    return render(request, 'library/members.html', {'members': members})

from django.shortcuts import redirect

def borrow_book(request, book_id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=book_id)
        member = Member.objects.get(email=request.user.email)  # Assuming email is used for login
        Borrowing.objects.create(book=book, member=member)
        return redirect('home')
    return redirect('login')

def return_book(request, borrowing_id):
    if request.user.is_authenticated:
        borrowing = Borrowing.objects.get(id=borrowing_id)
        borrowing.return_date = timezone.now()
        borrowing.save()
        return redirect('home')
    return redirect('login')

from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'library/profile.html', {'form': form})

@login_required
def notifications(request):
    user_member = Member.objects.get(email=request.user.email)
    notifications = Notification.objects.filter(member=user_member).order_by('-created_at')
    return render(request, 'library/notifications.html', {'notifications': notifications})
