# System Flow Diagram

## User Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Landing Page (/)                         │
│                  Browse All Books                            │
└────────────┬────────────────────────────────┬────────────────┘
             │                                │
             ▼                                ▼
    ┌────────────────┐              ┌────────────────┐
    │     Login      │              │  Student       │
    │   /login/      │              │  Signup        │
    └────────┬───────┘              │  /signup/      │
             │                      └────────┬───────┘
             │                               │
             ▼                               ▼
    ┌────────────────────────────────────────────────┐
    │         Authentication Check                    │
    │    (username, password, user type)             │
    └────────┬───────────────────────┬────────────────┘
             │                       │
             ▼                       ▼
    ┌────────────────┐      ┌────────────────┐
    │   Librarian    │      │    Student     │
    │   Dashboard    │      │   Dashboard    │
    └────────────────┘      └────────────────┘
```

## Librarian Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              Librarian Dashboard                             │
│  /librarian/dashboard/                                       │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Books   │ │ Students │ │ Requests │ │  Fines   │      │
│  │   Stats  │ │  Stats   │ │  Stats   │ │  Stats   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└────┬────────┬────────┬────────┬────────┬────────┬──────────┘
     │        │        │        │        │        │
     ▼        ▼        ▼        ▼        ▼        ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Manage  │ │Manage  │ │Manage  │ │ Book   │ │Issued  │ │ Fines  │
│ Books   │ │Catego- │ │Students│ │Requests│ │ Books  │ │ Mgmt   │
│         │ │ ries   │ │        │ │        │ │        │ │        │
└────┬────┘ └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘
     │           │          │          │          │          │
     ▼           ▼          ▼          ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  Add    │ │  Add    │ │  Add    │ │ Approve │ │ Return  │ │  View   │
│  Edit   │ │ Delete  │ │  Edit   │ │ Reject  │ │  Book   │ │  Fine   │
│ Delete  │ │Category │ │ Delete  │ │ Request │ │Calculate│ │ History │
│  Book   │ │         │ │ Student │ │         │ │  Fine   │ │         │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
     │
     ▼
┌─────────────────────────────────────┐
│   QR Code Auto-Generated on Save    │
│   Stored in media/qr_codes/         │
└─────────────────────────────────────┘
```

## Student Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              Student Dashboard                               │
│  /student/dashboard/                                         │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   Issued     │ │   Pending    │ │    Total     │       │
│  │    Books     │ │   Requests   │ │    Fines     │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└────┬─────────────────────┬─────────────────────┬───────────┘
     │                     │                     │
     ▼                     ▼                     ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Issued     │  │   Pending    │  │   Returned   │
│   Books      │  │   Requests   │  │   Books      │
│   Table      │  │   Table      │  │   & Fines    │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Book Request & Issue Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Student Actions                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Browse Books (/)    │
              │  Search Books        │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  View Book Details   │
              │  /book/<id>/         │
              │  - See QR Code       │
              │  - Check Availability│
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Request Book        │
              │  /book/<id>/request/ │
              └──────────┬───────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  BookIssue Created                           │
│                  Status: PENDING                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Librarian Reviews Request                       │
│              /librarian/requests/                            │
└────────┬────────────────────────────────────┬───────────────┘
         │                                    │
         ▼                                    ▼
┌────────────────┐                   ┌────────────────┐
│    APPROVE     │                   │    REJECT      │
└────────┬───────┘                   └────────┬───────┘
         │                                    │
         ▼                                    ▼
┌────────────────────────────┐      ┌────────────────┐
│  Status: ISSUED            │      │ Status:        │
│  issue_date = NOW          │      │ REJECTED       │
│  due_date = NOW + 7 days   │      └────────────────┘
│  available_copies -= 1     │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────┐
│  Student Has Book          │
│  (7 days to return)        │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────┐
│  Librarian Returns Book    │
│  /librarian/issued/        │
└────────┬───────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              Return Processing                               │
│                                                              │
│  IF return_date > due_date:                                 │
│      late_days = (return_date - due_date).days              │
│      fine = late_days × fine_per_day ($10)                  │
│  ELSE:                                                       │
│      fine = $0                                              │
│                                                              │
│  Status: RETURNED                                           │
│  available_copies += 1                                      │
└─────────────────────────────────────────────────────────────┘
```

## QR Code Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Librarian Adds New Book                         │
│              /librarian/books/add/                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Book.save() called  │
              └──────────┬───────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              QR Code Generation                              │
│                                                              │
│  1. Create QR data string:                                  │
│     "Book ID: {id}                                          │
│      Title: {title}                                         │
│      Author: {author}                                       │
│      Shelf: {shelf_no}                                      │
│      ISBN: {isbn}"                                          │
│                                                              │
│  2. Generate QR image using qrcode library                  │
│  3. Save as PNG: media/qr_codes/qr_{isbn}.png              │
│  4. Store path in book.qr_code field                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  QR Code Stored      │
              │  & Ready to Display  │
              └──────────┬───────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              QR Code Usage                                   │
│                                                              │
│  Display on:                                                │
│  - Book Detail Page (/book/<id>/)                           │
│  - Librarian Book Management                                │
│                                                              │
│  Scan QR → Redirects to /qr/<id>/ → /book/<id>/           │
└─────────────────────────────────────────────────────────────┘
```

## Search Flow

```
┌─────────────────────────────────────────────────────────────┐
│              User Enters Search Query                        │
│              (Home Page or Librarian Panel)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Django Query Filter                             │
│                                                              │
│  Book.objects.filter(                                       │
│      Q(title__icontains=query) |                            │
│      Q(author__icontains=query) |                           │
│      Q(isbn__icontains=query) |                             │
│      Q(shelf_no__icontains=query) |                         │
│      Q(category__name__icontains=query)                     │
│  )                                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Display Results     │
              │  (Filtered Books)    │
              └──────────────────────┘
```

## Fine Calculation Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Librarian Returns Book                          │
│              /librarian/issued/<id>/return/                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Set return_date     │
              │  = current datetime  │
              └──────────┬───────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Calculate Fine                                  │
│                                                              │
│  IF return_date > due_date:                                 │
│      late_days = (return_date - due_date).days              │
│      fine = late_days × fine_per_day                        │
│                                                              │
│      Example:                                               │
│      due_date = 2024-01-01                                  │
│      return_date = 2024-01-05                               │
│      late_days = 4                                          │
│      fine = 4 × $10 = $40                                   │
│                                                              │
│  ELSE:                                                       │
│      fine = $0 (returned on time)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Save Fine Amount    │
              │  Update Status       │
              │  Increment Available │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Display Fine        │
              │  in Dashboard        │
              └──────────────────────┘
```

## Database Relationships

```
┌──────────────┐
│     User     │
│ (AbstractUser)│
├──────────────┤
│ username     │
│ email        │
│ password     │
│ is_student   │
│ is_librarian │
└──────┬───────┘
       │
       │ OneToOne
       │
   ┌───┴────┬──────────┐
   │        │          │
   ▼        ▼          ▼
┌────────┐ ┌─────────┐
│Student │ │Librarian│
├────────┤ ├─────────┤
│full_name│ │ phone  │
│email   │ └─────────┘
│phone   │
│student_id│
└────┬───┘
     │
     │ ForeignKey
     │
     ▼
┌──────────────┐
│  BookIssue   │
├──────────────┤
│ student      │◄────┐
│ book         │     │
│ issue_date   │     │
│ due_date     │     │
│ return_date  │     │
│ status       │     │
│ fine         │     │
└──────────────┘     │
                     │ ForeignKey
                     │
                ┌────┴────┐
                │  Book   │
                ├─────────┤
                │ title   │
                │ author  │
                │ category│◄────┐
                │ shelf_no│     │
                │ isbn    │     │
                │ copies  │     │
                │ qr_code │     │
                └─────────┘     │
                                │ ForeignKey
                                │
                          ┌─────┴────┐
                          │ Category │
                          ├──────────┤
                          │  name    │
                          └──────────┘
```

## Status Transitions

```
BookIssue Status Flow:

    PENDING ──────┬──────► APPROVED ──────► ISSUED ──────► RETURNED
                  │
                  └──────► REJECTED

Details:
- PENDING: Student has requested the book
- APPROVED: Librarian approved (transitional, immediately becomes ISSUED)
- ISSUED: Book is with student (7-day countdown starts)
- RETURNED: Book returned (fine calculated if late)
- REJECTED: Librarian rejected the request
```

## Key Features Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    System Features                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✓ Dual User System (Librarian + Student)                  │
│  ✓ Complete Book Management (CRUD)                          │
│  ✓ Automatic QR Code Generation                            │
│  ✓ Book Request & Approval Workflow                         │
│  ✓ 7-Day Issue Period                                       │
│  ✓ Automatic Fine Calculation                               │
│  ✓ Multi-field Search                                       │
│  ✓ Category Management                                      │
│  ✓ Student Management                                       │
│  ✓ Overdue Tracking                                         │
│  ✓ Fine History                                             │
│  ✓ Dashboard Analytics                                      │
│  ✓ Responsive UI (Bootstrap 5)                              │
│  ✓ Role-based Access Control                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

This system flow provides a complete overview of how the Library Management System operates from user authentication through book management, requests, issues, returns, and fine calculations.
