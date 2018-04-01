from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from wordbucket.models import Word, Explanation, Like, Dislike
import string, csv, os, codecs
from django.http import HttpResponse
from io import TextIOWrapper

def home_page(request):
    d_message = ""
    words = Word.objects.order_by('-date_pub')[:5]
    alphabets = string.ascii_lowercase
    return render(request, 'home.html', {'words': words, 'd_message': d_message, 'alphabets': alphabets})

def view_word(request, word_id):
    d_message = ""
    word_ = Word.objects.get(id=word_id)
    like_ = Like.objects.all
    dislike_ = Dislike.objects.all
    return render(request, 'detail.html', {'word': word_, 'like': like_, 'dislike': dislike_, 'd_message': d_message})

def add_word(request):
    d_message = ""
    words = Word.objects.order_by('-date_pub')[:5]
    word_reference = str(request.POST['word_input'])
    explanation_reference = str(request.POST['explanation_input'])
    # query for duplicate word
    d_query = Word.objects.filter(word=word_reference)
    if (not d_query) and (word_reference != '') :
        word_ = Word.objects.create(word = request.POST['word_input'])
        explanation_ = Explanation.objects.create(explanation_text=request.POST['explanation_input'], votes_like = 0, votes_dislike = 0, word=word_)
        return redirect('/')
    else :
        word_ = Word.objects.get(word=word_reference)
        d_query2 = Explanation.objects.filter(explanation_text=explanation_reference, word=word_)
        if (word_reference != '') and (not d_query2) :
            # duplacate word id
            dword_id = Word.objects.get(word = word_reference)
            explanation_ = Explanation.objects.create(explanation_text=request.POST['explanation_input'], votes_like = 0, votes_dislike = 0, word=dword_id)
            d_message = "duplicate word, your explanation add to existing word."
        else :
            d_message = "please enter the word"
        alphabets = string.ascii_lowercase
        return render(request, 'home.html', {'words': words, 'd_message': d_message, 'alphabets': alphabets})

def add_explanation(request, word_id):
    word_ = Word.objects.get(id=word_id)
    explanation_reference = str(request.POST['explanation_input'])
    # query for duplicate explanation
    d_query = Explanation.objects.filter(explanation_text=explanation_reference, word=word_)
    if (not d_query) and (explanation_reference != '') :
        explanation_ = Explanation.objects.create(explanation_text=request.POST['explanation_input'], votes_like = 0, votes_dislike = 0, word=word_)
        return redirect('/%d/' % (word_.id,))
    else :
        d_message = "duplicate or null explanation, please enter new explanation."
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
    if request.user.is_authenticated:
        d_query = Like.objects.filter(user_like=request.user.username, explanation=explanation_)
        if not d_query :
            Like.objects.create(user_like=request.user.username, explanation=explanation_)
            selected_explanation = explanation_.like_set.all()
            vote_like_ = selected_explanation.count()
            explanation_.votes_like = vote_like_
            explanation_.save()
    return HttpResponseRedirect(reverse('wordbucket:detail', args=(explanation_.word.id,)))

def vote_dislike(request, explanation_id):
    explanation_ = Explanation.objects.get(id=explanation_id)    
    if request.user.is_authenticated:
        d_query = Dislike.objects.filter(user_dislike=request.user.username, explanation=explanation_)
        if not d_query :
            Dislike.objects.create(user_dislike=request.user.username, explanation=explanation_)
            selected_explanation = explanation_.dislike_set.all()
            vote_dislike_ = selected_explanation.count()
            explanation_.votes_dislike = vote_dislike_
            explanation_.save()
    return HttpResponseRedirect(reverse('wordbucket:detail', args=(explanation_.word.id,)))

# auth. part

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# csv part

def export_csv(request, word_id):
    output = []
    word_ = Word.objects.get(id=word_id)
    selected_word = word_.explanation_set.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['word', 'explanation'])
    
    for word in selected_word:
        output.append([word.word, word.explanation_text])

    writer.writerows(output)
    return response

def import_csv(request, word_id):
    word_ = Word.objects.get(id=word_id)
    if request.POST and request.FILES:
        csvfile = TextIOWrapper(request.FILES['csv_file'], encoding=request.encoding)
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            #duplicate explanation
            d_query = Explanation.objects.filter(explanation_text=row[1], word=word_)
            if (not d_query) and (row[1] != '') :
                explanation_ = Explanation.objects.create(explanation_text=row[1], votes_like = 0, votes_dislike = 0, word=word_)
    return HttpResponseRedirect(reverse('wordbucket:detail', args=(word_id,)))
