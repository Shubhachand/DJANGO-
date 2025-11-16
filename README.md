# Django Library Management System

A complete library management system with QR code integration, built with Django 5.2.8.

## Features

### Librarian Panel
- Custom admin dashboard (not Django default admin)
- Add/Edit/Delete books with automatic QR code generation
- Manage shelf/rack numbers
- Manage categories
- CRUD operations for students
- Approve/reject book requests
- Manage issued books
- Set max issue duration (7 days fixed)
- View and manage fines
- Track overdue books
- Dashboard analytics

### Student Portal
- Signup & Login
- View available books
- Search books by title, author, category, shelf number, or ISBN
- Request/book a book
- View issued books & return dates
- Automatic fine calculation for late returns
- View fine history

### QR Code Features
- Automatically generates QR code for every book
- QR code contains: Book ID, Title, Author, Shelf Number, ISBN
- Scan QR to view book details page
- Shows availability, description, shelf location
- Quick access to request/issue options

### Book Rules
- Books can be issued for 7 days maximum
- Late submission triggers automatic fine calculation ($10/day default)
- Students cannot request if available_copies = 0
- Students can only have one active request per book

## Setup Instructions

### 1. Clone and Setup Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Setup Demo Data (Optional but Recommended)

```bash
python manage.py setup_demo
```

This creates:
- Librarian account: `username=librarian, password=librarian123`
- Student account: `username=student1, password=student123`
- Sample categories and books with QR codes

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Default Login Credentials

### Librarian
- Username: `librarian`
- Password: `librarian123`

### Student
- Username: `student1`
- Password: `student123`

## Project Structure

```
myproject/
├── core/                          # Main application
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── forms.py                   # Form classes
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Admin configuration
│   ├── templates/core/            # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── student_signup.html
│   │   ├── student_dashboard.html
│   │   ├── book_detail.html
│   │   ├── librarian_base.html
│   │   ├── librarian_dashboard.html
│   │   ├── librarian_books.html
│   │   ├── librarian_categories.html
│   │   ├── librarian_students.html
│   │   ├── librarian_requests.html
│   │   ├── librarian_issued_books.html
│   │   └── librarian_fines.html
│   └── management/commands/
│       └── setup_demo.py          # Demo data setup
├── myproject/                     # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                         # Uploaded files (QR codes)
├── static/                        # Static files
├── manage.py
└── requirements.txt
```

## Database Models

### User (Custom User Model)
- Extends Django's AbstractUser
- Fields: username, email, password, is_student, is_librarian

### Student
- full_name, email, phone, student_id
- OneToOne relationship with User

### Librarian
- phone
- OneToOne relationship with User

### Category
- name

### Book
- title, author, category, shelf_no, isbn
- total_copies, available_copies
- description, added_date
- qr_code (auto-generated image)

### BookIssue
- student, book
- request_date, issue_date, due_date, return_date
- status (pending, approved, issued, returned, rejected)
- fine, fine_per_day

## Key Functionalities

### Authentication
- Separate login/signup for librarians and students
- Role-based access control

### Book Issue Workflow
1. Student requests a book
2. Librarian approves the request
3. System automatically sets:
   - issue_date = current date
   - due_date = issue_date + 7 days
4. Book's available_copies decrements

### Return Workflow
1. Librarian marks book as returned
2. System calculates fine if overdue:
   - fine = (late_days × fine_per_day)
3. Book's available_copies increments

### Search Feature
- Search by title, author, category, shelf number, or ISBN
- Available on both public homepage and librarian panel

### QR Code System
- Auto-generated when book is added
- Stored in media/qr_codes/
- Displays on book detail page
- Scan redirects to book detail page

## Technologies Used

- Django 5.2.8
- Python 3.13
- SQLite (default database)
- Bootstrap 5.3
- Font Awesome 6.4
- Pillow (image processing)
- qrcode (QR code generation)

## API Endpoints

### Public URLs
- `/` - Home page (book listing)
- `/login/` - Login page
- `/signup/` - Student signup
- `/book/<id>/` - Book detail page
- `/qr/<id>/` - QR scan redirect

### Student URLs
- `/student/dashboard/` - Student dashboard
- `/book/<id>/request/` - Request a book

### Librarian URLs
- `/librarian/dashboard/` - Librarian dashboard
- `/librarian/books/` - Manage books
- `/librarian/books/add/` - Add new book
- `/librarian/books/<id>/edit/` - Edit book
- `/librarian/books/<id>/delete/` - Delete book
- `/librarian/categories/` - Manage categories
- `/librarian/students/` - Manage students
- `/librarian/requests/` - View book requests
- `/librarian/issued/` - View issued books
- `/librarian/fines/` - View fines

## Customization

### Change Fine Amount
Edit `core/models.py` in the `BookIssue` model:
```python
fine_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
```

### Change Issue Duration
Edit `core/models.py` in the `approve_and_issue` method:
```python
self.due_date = self.issue_date + timedelta(days=7)  # Change 7 to desired days
```

## Notes

- QR codes are automatically generated when books are added
- Media files (QR codes) are stored in the `media/` directory
- The system uses Bootstrap 5 for responsive design
- All templates use Font Awesome icons for better UI/UX

## Support

For issues or questions, please check the code comments or Django documentation.
# DJANGO-
