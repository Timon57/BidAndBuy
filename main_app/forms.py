from .models import Category
from django.forms import ModelForm

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['is_active']