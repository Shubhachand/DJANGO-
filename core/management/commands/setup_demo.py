from django.core.management.base import BaseCommand
from core.models import User, Librarian, Student, Category, Book


class Command(BaseCommand):
    help = 'Setup demo data for the library system'

    def handle(self, *args, **kwargs):
        # Create librarian
        if not User.objects.filter(username='librarian').exists():
            librarian_user = User.objects.create_user(
                username='librarian',
                email='librarian@library.com',
                password='librarian123',
                is_librarian=True,
                is_staff=True
            )
            Librarian.objects.create(user=librarian_user, phone='1234567890')
            self.stdout.write(self.style.SUCCESS('Librarian created: username=librarian, password=librarian123'))
        
        # Create sample student
        if not User.objects.filter(username='student1').exists():
            student_user = User.objects.create_user(
                username='student1',
                email='student1@example.com',
                password='student123',
                is_student=True
            )
            Student.objects.create(
                user=student_user,
                full_name='John Doe',
                email='student1@example.com',
                phone='9876543210',
                student_id='STU001'
            )
            self.stdout.write(self.style.SUCCESS('Student created: username=student1, password=student123'))
        
        # Create categories
        categories_data = ['Fiction', 'Non-Fiction', 'Science', 'History', 'Technology', 'Biography']
        for cat_name in categories_data:
            Category.objects.get_or_create(name=cat_name)
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories_data)} categories'))
        
        # Create sample books
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'category': 'Fiction',
                'shelf_no': 'A-101',
                'isbn': '9780743273565',
                'total_copies': 5,
                'available_copies': 5,
                'description': 'A classic American novel set in the Jazz Age.'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'category': 'Fiction',
                'shelf_no': 'A-102',
                'isbn': '9780061120084',
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A gripping tale of racial injustice and childhood innocence.'
            },
            {
                'title': 'A Brief History of Time',
                'author': 'Stephen Hawking',
                'category': 'Science',
                'shelf_no': 'B-201',
                'isbn': '9780553380163',
                'total_copies': 4,
                'available_copies': 4,
                'description': 'A landmark volume in science writing.'
            },
            {
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'category': 'History',
                'shelf_no': 'C-301',
                'isbn': '9780062316097',
                'total_copies': 6,
                'available_copies': 6,
                'description': 'A brief history of humankind.'
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'category': 'Technology',
                'shelf_no': 'D-401',
                'isbn': '9780132350884',
                'total_copies': 4,
                'available_copies': 4,
                'description': 'A handbook of agile software craftsmanship.'
            },
        ]
        
        for book_data in books_data:
            category = Category.objects.get(name=book_data['category'])
            if not Book.objects.filter(isbn=book_data['isbn']).exists():
                Book.objects.create(
                    title=book_data['title'],
                    author=book_data['author'],
                    category=category,
                    shelf_no=book_data['shelf_no'],
                    isbn=book_data['isbn'],
                    total_copies=book_data['total_copies'],
                    available_copies=book_data['available_copies'],
                    description=book_data['description']
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(books_data)} sample books'))
        self.stdout.write(self.style.SUCCESS('\n=== Demo Setup Complete ==='))
        self.stdout.write(self.style.SUCCESS('Librarian Login: username=librarian, password=librarian123'))
        self.stdout.write(self.style.SUCCESS('Student Login: username=student1, password=student123'))
