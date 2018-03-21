from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from wordbucket.models import Word, Explanation, Like_and_dislike
import string

def home_page(request):
    d_message = ""
    words = Word.objects.order_by('-date_pub')[:5]
    alphabets = string.ascii_lowercase
    return render(request, 'home.html', {'words': words, 'd_message': d_message, 'alphabets': alphabets})

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
        explanation_ = Explanation.objects.create(explanation_text=request.POST['explanation_input'], word=word_)
        Like_and_dislike.objects.create(votes_like = 0, votes_dislike = 0, explanation = explanation_)
        return redirect('/')
    else :
        # duplacate word id
        dword_id = Word.objects.get(word = word_reference)
        explanation_ = Explanation.objects.create(explanation_text=request.POST['explanation_input'], word=dword_id)
        Like_and_dislike.objects.create(votes_like = 0, votes_dislike = 0, explanation = explanation_)
        d_message = "duplicate word, your explanation add to existing word."
        return render(request, 'home.html', {'words': words, 'd_message': d_message})

def add_explanation(request, word_id):
    word_ = Word.objects.get(id=word_id)
    explanation_reference = str(request.POST['explanation_input'])
    # query for duplicate explanation
    d_query = Explanation.objects.filter(explanation_text=explanation_reference)
    if not d_query :
        explanation_ = Explanation.objects.create(explanation_text=request.POST['explanation_input'], word=word_)
        Like_and_dislike.objects.create(votes_like = 0, votes_dislike = 0, explanation = explanation_)
        return redirect('/%d/' % (word_.id,))
    else :
        d_message = "duplicate explanation, please enter new explanation."
        return render(request, 'detail.html', {'word': word_, 'd_message': d_message})
        
def search(request, word_search):    
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
        word_found = Word.objects.filter(word__startswith=word_search)
        if not word_found :
            message = "WORD not found"
            return render(request, 'search.html', {'message': message})
        else :
            return render(request, 'search.html', {'word_found': word_found})

def vote_like(request, explanation_id):
    explanation_ = Explanation.objects.get(id=explanation_id)
    selected_explanation = explanation_.like_and_dislike_set.all()
    vote_like_ = selected_explanation.count()
    if vote_like_ == 0 :
        Like_and_dislike.objects.create(vote_like=1, explanation=explanation_)
    else :
        for voteslike in selected_explanation :
            voteslike.votes_like += 1
            voteslike.save()
        return HttpResponseRedirect(reverse('wordbucket:detail', args=(explanation_.word.id,)))
    

def vote_dislike(request, explanation_id):
    explanation_ = Explanation.objects.get(id=explanation_id)
    selected_explanation = explanation_.like_and_dislike_set.all()
    vote_dislike_ = selected_explanation.count()
    if vote_dislike_ == 0 :
        Like_and_dislike.objects.create(vote_dislike=1, explanation=explanation_)
    else :
        for votesdislike in selected_explanation :
            votesdislike.votes_dislike += 1
            votesdislike.save()
        return HttpResponseRedirect(reverse('wordbucket:detail', args=(explanation_.word.id,)))
