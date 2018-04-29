from django.core import mail

def send_confirmation(user, rental):
    mail.send_mail(
        'Rental Confirmation: {}'.format(user.username),
        'You have successfully rented {}, it is due on {}.'
            .format(rental.book.title, rental.due_date),
        'from@example.com',
        [user.email],
        fail_silently=False
    )
