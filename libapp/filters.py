import django_filters
from django_filters import CharFilter

from .models import *

class BookFilter(django_filters.FilterSet):
    
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['bname', 'bookdesc', 'price', 'stock', 'book_image']