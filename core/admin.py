from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Librarian, Book, Category, BookIssue


class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_student', 'is_librarian', 'is_staff']
    list_filter = ['is_student', 'is_librarian', 'is_staff', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Type', {'fields': ('is_student', 'is_librarian')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Librarian)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BookIssue)
