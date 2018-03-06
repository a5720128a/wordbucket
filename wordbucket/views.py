from django.shortcuts import redirect, render
from wordbucket.models import Word, Explanation, Like_and_dislike

def home_page(request):
    d_message = ""
    words = Word.objects.order_by('-date_pub')[:5]
    return render(request, 'home.html', {'words': words, 'd_message': d_message})

def view_word(request, word_id):
    d_message = ""
    word_ = Word.objects.get(id=word_id)
    return render(request, 'detail.html', {'word': word_, 'd_message': d_message})

def add_word(request):
    d_message = ""
    words = Word.objects.order_by('-date_pub')[:5]
    word_reference = str(request.POST['word_input'])
    # query for duplicate word
    d_query = Word.objects.filter(word=word_reference)
    if not d_query :
        word_ = Word.objects.create(word = request.POST['word_input'])
        Explanation.objects.create(explanation_text=request.POST['explanation_input'], word=word_)
        return redirect('/')
    else :
        # duplacate word id
        dword_id = Word.objects.get(word = word_reference)
        Explanation.objects.create(explanation_text=request.POST['explanation_input'], word=dword_id)
        d_message = "duplicate word, your explanation add to existing word."
        return render(request, 'home.html', {'words': words, 'd_message': d_message})

def add_explanation(request, word_id):
    word_ = Word.objects.get(id=word_id)
    explanation_reference = str(request.POST['explanation_input'])
    # query for duplicate explanation
    d_query = Explanation.objects.filter(explanation_text=explanation_reference)
    if not d_query :
        Explanation.objects.create(explanation_text=request.POST['explanation_input'], word=word_)
        return redirect('/%d/' % (word_.id,))
    else :
        d_message = "duplicate explanation, please enter new explanation."
        return render(request, 'detail.html', {'word': word_, 'd_message': d_message})
        
def search(request):    
    word_reference = 'no'
    if request.method == 'POST':
        word_reference = str(request.POST['search_input'])
    if word_reference != 'no' :
        word_found = Word.objects.filter(word__contains=word_reference)
        if not word_found :
            message = "WORD not found"
            return render(request, 'search.html', {'message': message})
        else :
            return render(request, 'search.html', {'word_found': word_found})
    else :
        return render(request, 'search.html')

def vote_like(request):
    pass

def vote_dislike(request):
    pass
