from django.shortcuts import redirect, render
from wordbucket.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(word=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
