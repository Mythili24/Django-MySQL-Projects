from django.forms import ModelForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


from .models import Book, IssueDetail, Member

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['bname', 'authorname', 'bookdesc', 'price', 'stock', 'book_category', 'book_image']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

MTYPE = (
            ('student', 'Student'),
            ('teacher', 'Teacher')
            )

class MemberForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    date_created = forms.DateTimeField()
    member_image = forms.ImageField()
    type = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,choices=MTYPE)
    
    class Meta:
        model = Member
        fields = '__all__'

            
class IssueDetailForm(forms.ModelForm):
    member_choices = Member.objects.all()
    member = forms.CharField(label='Member', widget=forms.Select(choices=member_choices))
    bname = forms.CharField(max_length=100)
    issue_date = forms.DateField()
    due_date = forms.DateField()

    class Meta:
        model = IssueDetail        
        fields = ['member', 'bname', 'issue_date', 'due_date']


#class IssueDetailForm(forms.ModelForm):
#    member = forms.ModelChoiceField(queryset=Member.objects.all())

#    class Meta:
#        model = IssueDetail        
#        fields = ['member', 'type', 'bname', 'issue_date', 'due_date']