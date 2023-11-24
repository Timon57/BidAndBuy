from django.shortcuts import render,get_object_or_404,redirect
from .models import Category
from .forms import CategoryForm


def category_list(request):
    category_list = Category.objects.all()
    context = {'category_list':category_list}
    return render(request,'main_app/category/category_list.html',context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
        context = {'form':form}
        return render(request,'main_app/category/category_create.html',context)
    
def category_update(request,pk):
    data = get_object_or_404(Category,id=pk)
    form = CategoryForm(instance=data)
    context = {'form':form}
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    return render(request,'main_app/category/category_update.html',context)

def category_delete(request,pk):
    data = get_object_or_404(Category,id=pk)
    data.is_active=False
    data.save()
    return redirect('category-list')
        

