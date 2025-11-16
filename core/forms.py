from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Book, Category, BookIssue


class StudentSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    student_id = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                student_id=self.cleaned_data['student_id']
            )
        return user


class LibrarianSignupForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_librarian = True
        user.is_staff = True
        if commit:
            user.save()
            from .models import Librarian
            Librarian.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', '')
            )
        return user


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'shelf_no', 'isbn', 'total_copies', 'available_copies', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = Student
        fields = ['full_name', 'email', 'phone', 'student_id']
    
    def __init__(self, *args, **kwargs):
        self.instance_user = kwargs.pop('instance_user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
    
    def save(self, commit=True):
        student = super().save(commit=False)
        
        if not student.user_id:
            # Creating new student
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data.get('password', 'defaultpass123'),
                is_student=True
            )
            student.user = user
        else:
            # Updating existing student
            user = student.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if self.cleaned_data.get('password'):
                user.set_password(self.cleaned_data['password'])
            user.save()
        
        if commit:
            student.save()
        return student


class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search by title, author, ISBN, category, or shelf number...',
        'class': 'form-control'
    }))
