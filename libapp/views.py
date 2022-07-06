from django.shortcuts import redirect, render
from django.http import HttpResponse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date
from django.utils.timesince import timesince

# Create your views here.
from .models import Book, Member, IssueDetail
from .forms import BookForm, CreateUserForm, MemberForm, IssueDetailForm
from .filters import BookFilter

#def index(request):
#    return HttpResponse("<h1>Welcome to National Library Management System</h1>")

def index(request):    
    return render(request, 'libapp/welcome.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)

                return redirect('/login/')

        context = {'form':form}
        return render(request, 'libapp/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/profile/')
            else:
                messages.info(request, 'Username OR Password is incorrect')
                
        context = {}
        return render(request, 'libapp/login.html', context)

def adminloginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/books')
            else:
                messages.info(request, 'Username OR Password is incorrect')
                
        context = {}
        return render(request, 'libapp/admin_login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')
    
#@login_required(login_url='/admin')
def books(request):
    book_list = Book.objects.all()
    myFilter = BookFilter(request.GET, queryset=book_list)
    book_list = myFilter.qs
    
    context = {'myFilter' : myFilter, 'book_list' : book_list}
    return render(request, 'libapp/index.html', context)

#@login_required(login_url='/admin')
def detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'libapp/detail.html', {'book': book})

#@login_required(login_url='/admin')
def add_book(request):
    if request.method == 'POST':
        bname = request.POST.get('bname',)
        authorname = request.POST.get('authorname',)
        bookdesc = request.POST.get('bookdesc',)
        price = request.POST.get('price',)
        stock = request.POST.get('stock',)
        book_category = request.POST.get('book_category',)
        book_image = request.FILES['book_image']

        book = Book(bname=bname, authorname=authorname, bookdesc=bookdesc, price=price, stock=stock, book_category=book_category, book_image=book_image)
        book.save()
                
    return render(request, 'libapp/add_book.html')

#@login_required(login_url='/admin')
def update(request, id):
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, request.FILES, instance=book)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'libapp/edit.html', {'form':form, 'book':book})

#@login_required(login_url='/admin')
def delete(request,id):
    if request.method=="POST":
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('/')
    return render(request,'libapp/delete.html')


#@login_required(login_url='/admin_login/')
def profile(request):
    return render(request, 'libapp/profile.html')

def member_detail(request, id):
    member = Member.objects.get(id=id)
    context = {'member' : member}
    return render(request, 'libapp/member_details.html', context)

def viewmember(request, user):
    member = Member.objects.get(name=user)
    context = {'member' : member}
    return render(request, 'libapp/viewmember.html', context)

#@login_required(login_url='/admin_login/')
def members(request):
    member_list = Member.objects.all()
    context = {'member_list' : member_list}
    return render(request, 'libapp/members.html', context)


#@login_required(login_url='/admin_login/')
def issue_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    li=[]
    details = IssueDetail.objects.filter(member_id=member)
    member_name = details.first()
#    member_type = member_name.type
    book_count = details.count()
    today = date.today()
    detail_list = list(IssueDetail.objects.filter(member_id=member))
    i=0
    for detail in detail_list:
        if detail_list[i].due_date < today:
            t=(detail_list[i].id,
                detail_list[i].bname,
                detail_list[i].issue_date,
                detail_list[i].due_date,
                'Due Date has crossed by',
                (today-detail_list[i].due_date).days,
                ((today-detail_list[i].due_date).days)*2)
        else:
            t=(detail_list[i].id,
                detail_list[i].bname,
                detail_list[i].issue_date,
                detail_list[i].due_date,
                'Due Date is yet to come',
                (detail_list[i].due_date-today).days,
                0)
        i=i+1
        li.append(t)
    context = {'details': details, 'book_count': book_count, 'member_name': member_name, 
                'today':today, 'li':li}
    return render(request, 'libapp/issue_detailsnew.html', context)    


#@login_required(login_url='/admin_login/')
def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name',)
        email = request.POST.get('email',)
        phone = request.POST.get('phone',)
        date_created = request.POST.get('date_created',)    
        type = request.POST.get('type',)
        member_image = request.FILES['member_image']

        member = Member(name=name, email=email, phone=phone, date_created=date_created, type=type, member_image=member_image)
        member.save()
        
    return render(request, 'libapp/add_member.html')

#@login_required(login_url='/admin_login/')
def update_member(request, id):
    member = Member.objects.get(id=id)
    form = MemberForm(request.POST or None, request.FILES, instance=member)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'libapp/update_member.html', {'form':form, 'member':member})

#@login_required(login_url='/admin_login/')
def delete_member(request,id):
    if request.method=="POST":
        member = Member.objects.get(id=id)
        member.delete()
        return redirect('/')
    return render(request,'libapp/delete_member.html')

#@login_required(login_url='/admin_login/')
def issue_book(request, member_id):
    member_list = Member.objects.all()
    newmember = member_list.get(id=member_id)
    if request.method == 'POST':
        
        bname = request.POST.get('bname',)
        issue_date = request.POST.get('issue_date',)
        due_date = request.POST.get('due_date',)
        
        detail = IssueDetail.objects.create(member=newmember, bname=bname, issue_date=issue_date, due_date=due_date)
        detail.save()   
        messages.success(request, "Book issued successfully")
        
    return render(request, 'libapp/issue_book.html', {'member_list':member_list, 'messages':messages})

#@login_required(login_url='/admin_login/')
def return_book(request, id):
    if request.method=="POST":
        detail = IssueDetail.objects.get(id=id)
        detail.delete()
        return redirect('/')
    return render(request,'libapp/return_book.html')


#def search(request):
#    if request.method=="POST":
#        searched = request.POST['searched']
#        authors = Book.objects.filter(authorname__contains=searched)
#        return render(request, 'libapp/search.html', {'searched':searched, 'authors':authors})
#    else:
#        return render(request, 'libapp/search.html', {})
    
    