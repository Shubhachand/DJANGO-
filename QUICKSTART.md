# Quick Start Guide

## Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Setup Database & Demo Data
```bash
python manage.py migrate
python manage.py setup_demo
```

### Step 3: Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Login Credentials

**Librarian:**
- Username: `librarian`
- Password: `librarian123`
- Access: http://127.0.0.1:8000/librarian/dashboard/

**Student:**
- Username: `student1`
- Password: `student123`
- Access: http://127.0.0.1:8000/student/dashboard/

## What to Try

### As Librarian:
1. Login with librarian credentials
2. Add new books (QR codes auto-generate!)
3. Manage categories
4. Add/edit students
5. Approve book requests
6. Issue and return books
7. View fines for overdue books

### As Student:
1. Login with student credentials
2. Browse available books
3. Search for books
4. Request a book
5. View your issued books
6. Check due dates and fines

### QR Code Feature:
1. Go to any book detail page
2. See the QR code on the right side
3. The QR code contains book information
4. Scanning it redirects to the book detail page

## Common Tasks

### Add a New Book
1. Login as librarian
2. Go to "Manage Books"
3. Click "Add New Book"
4. Fill in details (QR code generates automatically)
5. Save

### Issue a Book
1. Student requests a book from the homepage
2. Librarian goes to "Book Requests"
3. Click "Approve" on the request
4. Book is automatically issued for 7 days

### Return a Book
1. Librarian goes to "Issued Books"
2. Click "Return" on the book
3. If overdue, fine is automatically calculated

### Search Books
- Use the search bar on homepage
- Search by: title, author, ISBN, category, or shelf number

## File Locations

- **QR Codes:** `media/qr_codes/`
- **Database:** `db.sqlite3`
- **Templates:** `core/templates/core/`
- **Static Files:** `static/`

## Troubleshooting

**Port already in use?**
```bash
python manage.py runserver 8001
```

**Need to reset database?**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py setup_demo
```

**Create your own admin?**
```bash
python manage.py createsuperuser
```

## Next Steps

- Customize fine amounts in `core/models.py`
- Add more books and categories
- Create additional student accounts
- Explore the QR code functionality
- Customize templates in `core/templates/core/`

Enjoy your Library Management System! 📚
