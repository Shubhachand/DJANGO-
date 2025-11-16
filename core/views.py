from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from .models import Book, Student, Category, BookIssue, User
from .forms import StudentSignupForm, BookForm, CategoryForm, StudentForm, BookSearchForm


def home(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    search_form = BookSearchForm(request.GET)
    
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data['query']
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(shelf_no__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = {
        'books': books,
        'categories': categories,
        'search_form': search_form,
    }
    return render(request, 'core/home.html', context)


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = StudentSignupForm()
    return render(request, 'core/student_signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_librarian:
                return redirect('librarian_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    can_request = False
    
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
        # Check if student already has pending or issued request for this book
        existing_request = BookIssue.objects.filter(
            student=student,
            book=book,
            status__in=['pending', 'issued']
        ).exists()
        can_request = not existing_request and book.available_copies > 0
    
    context = {
        'book': book,
        'can_request': can_request,
    }
    return render(request, 'core/book_detail.html', context)


@login_required
def request_book(request, book_id):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Only students can request books')
        return redirect('book_detail', book_id=book_id)
    
    book = get_object_or_404(Book, id=book_id)
    student = request.user.student_profile
    
    # Check if book is available
    if book.available_copies <= 0:
        messages.error(request, 'This book is not available')
        return redirect('book_detail', book_id=book_id)
    
    # Check if student already has pending/issued request
    existing = BookIssue.objects.filter(
        student=student,
        book=book,
        status__in=['pending', 'issued']
    ).exists()
    
    if existing:
        messages.error(request, 'You already have a pending or active request for this book')
        return redirect('book_detail', book_id=book_id)
    
    # Create request
    BookIssue.objects.create(student=student, book=book, status='pending')
    messages.success(request, 'Book request submitted successfully!')
    return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    student = request.user.student_profile
    issued_books = BookIssue.objects.filter(student=student, status='issued')
    pending_requests = BookIssue.objects.filter(student=student, status='pending')
    returned_books = BookIssue.objects.filter(student=student, status='returned')
    total_fines = sum(book.fine for book in returned_books)
    
    context = {
        'student': student,
        'issued_books': issued_books,
        'pending_requests': pending_requests,
        'returned_books': returned_books,
        'total_fines': total_fines,
    }
    return render(request, 'core/student_dashboard.html', context)


# Librarian Views
@login_required
def librarian_dashboard(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    total_books = Book.objects.count()
    total_students = Student.objects.count()
    pending_requests = BookIssue.objects.filter(status='pending').count()
    issued_books = BookIssue.objects.filter(status='issued').count()
    overdue_books = BookIssue.objects.filter(
        status='issued',
        due_date__lt=timezone.now()
    ).count()
    
    recent_requests = BookIssue.objects.filter(status='pending').order_by('-request_date')[:5]
    
    context = {
        'total_books': total_books,
        'total_students': total_students,
        'pending_requests': pending_requests,
        'issued_books': issued_books,
        'overdue_books': overdue_books,
        'recent_requests': recent_requests,
    }
    return render(request, 'core/librarian_dashboard.html', context)


from django.utils import timezone


@login_required
def librarian_books(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    books = Book.objects.all().order_by('-added_date')
    search_form = BookSearchForm(request.GET)
    
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data['query']
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(shelf_no__icontains=query)
        )
    
    return render(request, 'core/librarian_books.html', {'books': books, 'search_form': search_form})


@login_required
def librarian_add_book(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('librarian_books')
    else:
        form = BookForm()
    
    return render(request, 'core/librarian_book_form.html', {'form': form, 'action': 'Add'})


@login_required
def librarian_edit_book(request, book_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('librarian_books')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'core/librarian_book_form.html', {'form': form, 'action': 'Edit', 'book': book})


@login_required
def librarian_delete_book(request, book_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('librarian_books')
    
    return render(request, 'core/librarian_book_delete.html', {'book': book})


@login_required
def librarian_categories(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('librarian_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'core/librarian_categories.html', {'categories': categories, 'form': form})


@login_required
def librarian_delete_category(request, category_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('librarian_categories')


@login_required
def librarian_students(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    students = Student.objects.all()
    return render(request, 'core/librarian_students.html', {'students': students})


@login_required
def librarian_add_student(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('librarian_students')
    else:
        form = StudentForm()
    
    return render(request, 'core/librarian_student_form.html', {'form': form, 'action': 'Add'})


@login_required
def librarian_edit_student(request, student_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student, instance_user=student.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('librarian_students')
    else:
        form = StudentForm(instance=student, instance_user=student.user)
    
    return render(request, 'core/librarian_student_form.html', {'form': form, 'action': 'Edit', 'student': student})


@login_required
def librarian_delete_student(request, student_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('librarian_students')
    
    return render(request, 'core/librarian_student_delete.html', {'student': student})


@login_required
def librarian_requests(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    pending_requests = BookIssue.objects.filter(status='pending').order_by('-request_date')
    return render(request, 'core/librarian_requests.html', {'requests': pending_requests})


@login_required
def librarian_approve_request(request, request_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    book_issue = get_object_or_404(BookIssue, id=request_id)
    
    if book_issue.approve_and_issue():
        messages.success(request, 'Book issued successfully!')
    else:
        messages.error(request, 'Book not available')
    
    return redirect('librarian_requests')


@login_required
def librarian_reject_request(request, request_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    book_issue = get_object_or_404(BookIssue, id=request_id)
    book_issue.status = 'rejected'
    book_issue.save()
    messages.success(request, 'Request rejected')
    return redirect('librarian_requests')


@login_required
def librarian_issued_books(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    issued_books = BookIssue.objects.filter(status='issued').order_by('due_date')
    return render(request, 'core/librarian_issued_books.html', {'issued_books': issued_books})


@login_required
def librarian_return_book(request, issue_id):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    book_issue = get_object_or_404(BookIssue, id=issue_id)
    book_issue.return_book()
    
    if book_issue.fine > 0:
        messages.warning(request, f'Book returned with fine: ${book_issue.fine}')
    else:
        messages.success(request, 'Book returned successfully!')
    
    return redirect('librarian_issued_books')


@login_required
def librarian_fines(request):
    if not request.user.is_librarian:
        messages.error(request, 'Access denied')
        return redirect('home')
    
    fines = BookIssue.objects.filter(fine__gt=0).order_by('-return_date')
    total_fines = sum(f.fine for f in fines)
    
    return render(request, 'core/librarian_fines.html', {'fines': fines, 'total_fines': total_fines})


@login_required
def qr_scan(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return redirect('book_detail', book_id=book.id)
