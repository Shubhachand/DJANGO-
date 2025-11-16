# URL Reference Guide

Complete list of all URLs in the Django Library Management System.

## 🌐 Public URLs (No Login Required)

### Homepage & Books
```
GET  /                          Home page - Browse all books
GET  /book/<int:book_id>/       Book detail page with QR code
GET  /qr/<int:book_id>/         QR code redirect to book detail
```

### Authentication
```
GET  /login/                    Login page
POST /login/                    Process login
GET  /signup/                   Student signup page
POST /signup/                   Process student registration
GET  /logout/                   Logout and redirect to home
```

## 👨‍🎓 Student URLs (Login Required)

### Dashboard
```
GET  /student/dashboard/        Student dashboard
                                - View issued books
                                - View pending requests
                                - View fines
                                - View return history
```

### Book Actions
```
GET  /book/<int:book_id>/request/   Request a book
                                     - Creates BookIssue with status='pending'
```

## 👨‍💼 Librarian URLs (Login Required, Librarian Only)

### Dashboard
```
GET  /librarian/dashboard/      Librarian dashboard
                                - Total books count
                                - Total students count
                                - Pending requests count
                                - Issued books count
                                - Overdue books count
                                - Recent requests list
```

### Book Management
```
GET  /librarian/books/                  List all books with search
POST /librarian/books/                  Search books
GET  /librarian/books/add/              Add new book form
POST /librarian/books/add/              Create new book (QR auto-generated)
GET  /librarian/books/<int:book_id>/edit/    Edit book form
POST /librarian/books/<int:book_id>/edit/    Update book
GET  /librarian/books/<int:book_id>/delete/  Delete confirmation
POST /librarian/books/<int:book_id>/delete/  Delete book
```

### Category Management
```
GET  /librarian/categories/                      List all categories
POST /librarian/categories/                      Add new category
GET  /librarian/categories/<int:category_id>/delete/  Delete category
```

### Student Management
```
GET  /librarian/students/                        List all students
GET  /librarian/students/add/                    Add student form
POST /librarian/students/add/                    Create student
GET  /librarian/students/<int:student_id>/edit/  Edit student form
POST /librarian/students/<int:student_id>/edit/  Update student
GET  /librarian/students/<int:student_id>/delete/    Delete confirmation
POST /librarian/students/<int:student_id>/delete/    Delete student
```

### Book Request Management
```
GET  /librarian/requests/                        List pending requests
GET  /librarian/requests/<int:request_id>/approve/   Approve request
                                                      - Sets status='issued'
                                                      - Sets issue_date
                                                      - Sets due_date (+7 days)
                                                      - Decrements available_copies
GET  /librarian/requests/<int:request_id>/reject/    Reject request
                                                      - Sets status='rejected'
```

### Issued Books Management
```
GET  /librarian/issued/                          List all issued books
GET  /librarian/issued/<int:issue_id>/return/    Return book
                                                  - Sets return_date
                                                  - Calculates fine if late
                                                  - Sets status='returned'
                                                  - Increments available_copies
```

### Fine Management
```
GET  /librarian/fines/              List all fines
                                    - Shows fine history
                                    - Total fines collected
```

## 📊 URL Patterns Summary

### By HTTP Method

**GET Requests (Read Operations):**
- 25 GET endpoints
- Used for displaying pages, lists, and forms

**POST Requests (Write Operations):**
- 10 POST endpoints
- Used for creating, updating, and deleting data

### By User Role

**Public (No Auth):** 5 URLs
- Home, book detail, QR scan, login, signup

**Student (Auth Required):** 2 URLs
- Dashboard, request book

**Librarian (Auth + Role):** 23 URLs
- Dashboard, books, categories, students, requests, issued, fines

## 🔗 URL Examples

### Public Access
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/book/1/
http://127.0.0.1:8000/qr/1/
http://127.0.0.1:8000/login/
http://127.0.0.1:8000/signup/
```

### Student Access
```
http://127.0.0.1:8000/student/dashboard/
http://127.0.0.1:8000/book/1/request/
```

### Librarian Access
```
http://127.0.0.1:8000/librarian/dashboard/
http://127.0.0.1:8000/librarian/books/
http://127.0.0.1:8000/librarian/books/add/
http://127.0.0.1:8000/librarian/books/1/edit/
http://127.0.0.1:8000/librarian/categories/
http://127.0.0.1:8000/librarian/students/
http://127.0.0.1:8000/librarian/requests/
http://127.0.0.1:8000/librarian/issued/
http://127.0.0.1:8000/librarian/fines/
```

## 🔐 Access Control

### Public URLs (No Authentication)
- `/` - Home
- `/book/<id>/` - Book detail
- `/qr/<id>/` - QR redirect
- `/login/` - Login
- `/signup/` - Signup

### Protected URLs (Login Required)
All other URLs require authentication via `@login_required` decorator

### Role-Based URLs (Librarian Only)
All `/librarian/*` URLs check `user.is_librarian` and redirect if false

### Role-Based URLs (Student Only)
All `/student/*` URLs check `hasattr(user, 'student_profile')` and redirect if false

## 📝 URL Naming Convention

All URLs have named patterns for easy reference in templates:

```python
# Public
'home'                      → /
'book_detail'              → /book/<id>/
'qr_scan'                  → /qr/<id>/
'login'                    → /login/
'student_signup'           → /signup/
'logout'                   → /logout/

# Student
'student_dashboard'        → /student/dashboard/
'request_book'             → /book/<id>/request/

# Librarian
'librarian_dashboard'      → /librarian/dashboard/
'librarian_books'          → /librarian/books/
'librarian_add_book'       → /librarian/books/add/
'librarian_edit_book'      → /librarian/books/<id>/edit/
'librarian_delete_book'    → /librarian/books/<id>/delete/
'librarian_categories'     → /librarian/categories/
'librarian_delete_category'→ /librarian/categories/<id>/delete/
'librarian_students'       → /librarian/students/
'librarian_add_student'    → /librarian/students/add/
'librarian_edit_student'   → /librarian/students/<id>/edit/
'librarian_delete_student' → /librarian/students/<id>/delete/
'librarian_requests'       → /librarian/requests/
'librarian_approve_request'→ /librarian/requests/<id>/approve/
'librarian_reject_request' → /librarian/requests/<id>/reject/
'librarian_issued_books'   → /librarian/issued/
'librarian_return_book'    → /librarian/issued/<id>/return/
'librarian_fines'          → /librarian/fines/
```

## 🎯 Usage in Templates

Use named URLs in templates with `{% url %}` tag:

```django
<!-- Link to home -->
<a href="{% url 'home' %}">Home</a>

<!-- Link to book detail -->
<a href="{% url 'book_detail' book.id %}">View Book</a>

<!-- Link to librarian dashboard -->
<a href="{% url 'librarian_dashboard' %}">Dashboard</a>

<!-- Link to edit book -->
<a href="{% url 'librarian_edit_book' book.id %}">Edit</a>
```

## 🔄 Redirects

### After Login
- Librarian → `/librarian/dashboard/`
- Student → `/` (home)

### After Logout
- All users → `/` (home)

### After Signup
- Student → `/` (home) with auto-login

### After Actions
- Add book → `/librarian/books/`
- Edit book → `/librarian/books/`
- Delete book → `/librarian/books/`
- Add student → `/librarian/students/`
- Approve request → `/librarian/requests/`
- Return book → `/librarian/issued/`
- Request book → `/student/dashboard/`

## 🚫 Error Handling

### 404 Not Found
- Invalid book ID
- Invalid student ID
- Invalid request ID

### 403 Forbidden
- Student accessing librarian URLs
- Librarian accessing student-only URLs
- Unauthenticated user accessing protected URLs

### Redirects with Messages
- Access denied → Redirect to home with error message
- Invalid action → Redirect to previous page with error message
- Success action → Redirect to list page with success message

## 📱 API-Style URLs (Future Enhancement)

Currently, the system uses traditional Django views. For API endpoints, consider adding:

```
/api/books/                 GET - List books
/api/books/<id>/            GET - Book detail
/api/books/                 POST - Create book
/api/books/<id>/            PUT - Update book
/api/books/<id>/            DELETE - Delete book
/api/students/              GET - List students
/api/requests/              GET - List requests
/api/requests/<id>/approve/ POST - Approve request
```

## 🔍 Search URLs

Search is implemented via GET parameters:

```
/?query=python              Search books on home page
/librarian/books/?query=python   Search books in librarian panel
```

## 📊 Statistics

- **Total URLs:** 30+
- **Public URLs:** 5
- **Student URLs:** 2
- **Librarian URLs:** 23
- **GET Endpoints:** 25
- **POST Endpoints:** 10
- **Named Patterns:** 30

## 🎯 Quick Reference Table

| URL Pattern | Method | Auth | Role | Purpose |
|------------|--------|------|------|---------|
| `/` | GET | No | Any | Home page |
| `/book/<id>/` | GET | No | Any | Book detail |
| `/login/` | GET/POST | No | Any | Login |
| `/signup/` | GET/POST | No | Any | Student signup |
| `/student/dashboard/` | GET | Yes | Student | Student dashboard |
| `/book/<id>/request/` | GET | Yes | Student | Request book |
| `/librarian/dashboard/` | GET | Yes | Librarian | Librarian dashboard |
| `/librarian/books/` | GET | Yes | Librarian | List books |
| `/librarian/books/add/` | GET/POST | Yes | Librarian | Add book |
| `/librarian/requests/` | GET | Yes | Librarian | List requests |
| `/librarian/issued/` | GET | Yes | Librarian | List issued books |
| `/librarian/fines/` | GET | Yes | Librarian | List fines |

---

**For complete URL configuration, see:** `core/urls.py` and `myproject/urls.py`
