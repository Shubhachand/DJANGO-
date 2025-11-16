from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('signup/', views.student_signup, name='student_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/request/', views.request_book, name='request_book'),
    path('qr/<int:book_id>/', views.qr_scan, name='qr_scan'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Librarian URLs
    path('librarian/dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/books/', views.librarian_books, name='librarian_books'),
    path('librarian/books/add/', views.librarian_add_book, name='librarian_add_book'),
    path('librarian/books/<int:book_id>/edit/', views.librarian_edit_book, name='librarian_edit_book'),
    path('librarian/books/<int:book_id>/delete/', views.librarian_delete_book, name='librarian_delete_book'),
    path('librarian/categories/', views.librarian_categories, name='librarian_categories'),
    path('librarian/categories/<int:category_id>/delete/', views.librarian_delete_category, name='librarian_delete_category'),
    path('librarian/students/', views.librarian_students, name='librarian_students'),
    path('librarian/students/add/', views.librarian_add_student, name='librarian_add_student'),
    path('librarian/students/<int:student_id>/edit/', views.librarian_edit_student, name='librarian_edit_student'),
    path('librarian/students/<int:student_id>/delete/', views.librarian_delete_student, name='librarian_delete_student'),
    path('librarian/requests/', views.librarian_requests, name='librarian_requests'),
    path('librarian/requests/<int:request_id>/approve/', views.librarian_approve_request, name='librarian_approve_request'),
    path('librarian/requests/<int:request_id>/reject/', views.librarian_reject_request, name='librarian_reject_request'),
    path('librarian/issued/', views.librarian_issued_books, name='librarian_issued_books'),
    path('librarian/issued/<int:issue_id>/return/', views.librarian_return_book, name='librarian_return_book'),
    path('librarian/fines/', views.librarian_fines, name='librarian_fines'),
]
