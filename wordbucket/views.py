from django.shortcuts import redirect, render
from wordbucket.models import Word, Explanation, Like_and_dislike

def home_page(request):
    if request.method == 'POST':
        word_ = Word.objects.create(word=request.POST['word_input'])
        Explanation.objects.create(explanation_text=request.POST['explanation_input'], word=word_)
        return redirect('/')

    words = Word.objects.all()
    return render(request, 'home.html', {'words': words})
