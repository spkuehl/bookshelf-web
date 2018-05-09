from itertools import islice
from bookshelf.users.models import User
from books.models import Book

def book_create_database():
    batch_size = 10
    objs = (Book(title='Endless Stories %s' % i) for i in range(10))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Book.objects.bulk_create(batch, batch_size)

def user_create_database():
    User.objects.create_superuser(username='admin_user',
                                         password='admin_pass',
                                         email='admin_email@test.com')
    batch_size = 1
    objs = (User(username='U %s' % i, password='upass') for i in range(10))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        User.objects.bulk_create(batch, batch_size)
