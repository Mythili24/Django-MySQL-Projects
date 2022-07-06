from datetime import datetime, timedelta
from django.db import models

# Create your models here.

class Book(models.Model):

    def __str__(self):
        return self.bname

    bname = models.CharField(max_length=100)
    authorname = models.CharField(max_length=100, null=True)
    bookdesc = models.CharField(max_length=255, null=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    book_category = models.CharField(max_length=20, null=True)
    book_image = models.ImageField(default='default.jpg', upload_to='book_images/')


class Member(models.Model):

    def __str__(self):
        return self.name

    MTYPE = (
            ('student', 'Student'),
            ('teacher', 'Teacher')
            )

    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    type = models.CharField(max_length=7, choices=MTYPE, default='Student')
    member_image = models.ImageField(default='default.jpg', upload_to='book_images/')    


def get_duedate():
    return datetime.today() + timedelta(days=15)
class IssueDetail(models.Model):
    
    def __str__(self):
        return str(self.member)

    member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    bname = models.CharField(max_length=100, null=True)
    issue_date = models.DateField()
    due_date = models.DateField(default=get_duedate)
    
    

#class Staff(models.Model):

#    staffid = models.IntegerField(default=0, null=True)
#    staffname = models.CharField(max_length=100)
#    loginid = models.CharField(default=' ', max_length=20, null=True)
#    loginpwd = models.CharField(default=' ', max_length=20, null=True)

