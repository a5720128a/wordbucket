from django.shortcuts import redirect, render
from wordbucket.models import Word

def home_page(request):
    if request.method == 'POST':
        Word.objects.create(word=request.POST['word_text'])
        return redirect('/')

    words = Word.objects.all()
    return render(request, 'home.html', {'words': words})
