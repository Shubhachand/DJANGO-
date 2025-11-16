from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files import File


class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='librarian_profile')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    student_id = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    shelf_no = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Generate QR code
        if not self.qr_code:
            qr_data = f"Book ID: {self.id}\nTitle: {self.title}\nAuthor: {self.author}\nShelf: {self.shelf_no}\nISBN: {self.isbn}"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            file_name = f'qr_{self.isbn}.png'
            self.qr_code.save(file_name, File(buffer), save=False)
        
        super().save(*args, **kwargs)


class BookIssue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='book_issues')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    request_date = models.DateTimeField(auto_now_add=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fine_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    
    def __str__(self):
        return f"{self.student.full_name} - {self.book.title}"
    
    def calculate_fine(self):
        if self.return_date and self.due_date:
            if self.return_date > self.due_date:
                late_days = (self.return_date - self.due_date).days
                self.fine = late_days * self.fine_per_day
                self.save()
        return self.fine
    
    def approve_and_issue(self):
        if self.book.available_copies > 0:
            self.status = 'issued'
            self.issue_date = timezone.now()
            self.due_date = self.issue_date + timedelta(days=7)
            self.book.available_copies -= 1
            self.book.save()
            self.save()
            return True
        return False
    
    def return_book(self):
        self.return_date = timezone.now()
        self.status = 'returned'
        self.book.available_copies += 1
        self.book.save()
        self.calculate_fine()
        self.save()
