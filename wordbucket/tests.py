from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from wordbucket.views import home_page  
from wordbucket.models import Word, Explanation, Like_and_dislike

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')  

        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Word Bucket</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')
    
    def test_displays_all_list_words(self):
        Word.objects.create(word='wordey 1')
        Word.objects.create(word='wordey 2')

        response = self.client.get('/')

        self.assertIn('wordey 1', response.content.decode())
        self.assertIn('wordey 2', response.content.decode())


class AllAroundModelsTest(TestCase):

    def test_saving_and_retrieving_words(self):

        word_ = Word()
        word_.save()
        
        first_explanation = Explanation()
        first_explanation.explanation_text = 'The first (ever) word explanation'
        first_explanation.word = word_
        first_explanation.save()

        second_explanation = Explanation()
        second_explanation.explanation_text = 'Explanation the second'
        second_explanation.word = word_
        second_explanation.save()

        saved_word = Word.objects.first()
        self.assertEqual(saved_word, word_)

        saved_explanations = Explanation.objects.all()
        self.assertEqual(saved_explanations.count(), 2)

        first_saved_explanation = saved_explanations[0]
        second_saved_explanation = saved_explanations[1]
        self.assertEqual(first_saved_explanation.explanation_text, 'The first (ever) word explanation')
        self.assertEqual(first_saved_explanation.word, word_)
        self.assertEqual(second_saved_explanation.explanation_text, 'Explanation the second')
        self.assertEqual(second_saved_explanation.word, word_)

    def test_saving_and_retrieving_like_and_dislike(self):

        word_ = Word()
        word_.save()
        
        explanation_ = Explanation()
        explanation_.explanation_text = 'test'
        explanation_.word = word_
        explanation_.save()

        first_votes_like = Like_and_dislike()
        first_votes_like.votes_like = 1
        first_votes_like.explanation = explanation_
        first_votes_like.save()

        second_votes_dislike = Like_and_dislike()
        second_votes_dislike.votes_dislike = 2
        second_votes_dislike.explanation = explanation_
        second_votes_dislike.save()

        saved_explanation = Explanation.objects.first()
        self.assertEqual(saved_explanation, explanation_)

        saved_likes_and_dislikes = Like_and_dislike.objects.all()
        self.assertEqual(saved_likes_and_dislikes.count(), 2)

        first_saved_votes_like = saved_likes_and_dislikes[0]
        second_saved_votes_like = saved_likes_and_dislikes[1]
        self.assertEqual(first_saved_votes_like.votes_like, 1)
        self.assertEqual(first_saved_votes_like.explanation, explanation_)
        self.assertEqual(second_saved_votes_like.votes_dislike, 2)
        self.assertEqual(second_saved_votes_like.explanation, explanation_)

class WordViewTest(TestCase):
    
    def test_passes_correct_word_to_template(self):
        other_word = Word.objects.create()
        correct_word = Word.objects.create()
        response = self.client.get('/%d/' % (correct_word.id,))
        self.assertEqual(response.context['word'], correct_word)

    def test_uses_word_template(self): # detail page
        word_ = Word.objects.create()
        response = self.client.get('/%d/' % (word_.id,))
        self.assertTemplateUsed(response, 'detail.html')


    def test_displays_only_explanation_for_that_word(self):
        correct_word = Word.objects.create()
        Explanation.objects.create(explanation_text='itemey 1', word=correct_word)
        Explanation.objects.create(explanation_text='itemey 2', word=correct_word)
        other_word = Word.objects.create()
        Explanation.objects.create(explanation_text='other word item 1', word=other_word)
        Explanation.objects.create(explanation_text='other word item 2', word=other_word)

        response = self.client.get('/%d/' % (correct_word.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other word item 1')
        self.assertNotContains(response, 'other word item 2')

class NewWordTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        self.client.post('/add_word', data={'word_input': 'A new list word','explanation_input': 'yes it is'})

        self.assertEqual(Word.objects.count(), 1)
        self.assertEqual(Explanation.objects.count(), 1)
        new_word = Word.objects.first()
        self.assertEqual(new_word.word, 'A new list word')


    def test_redirects_after_POST(self):
        response = self.client.post('/add_word', data={'word_input': 'A new list word','explanation_input': 'yes it is'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

class NewExplanationTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_existing_word(self):
        other_word = Word.objects.create()
        correct_word = Word.objects.create()

        self.client.post(
            '/%d/add_explanation' % (correct_word.id,),
            data={'explanation_input': 'A new explanation for an existing word'}
        )

        self.assertEqual(Explanation.objects.count(), 1)
        new_explanation = Explanation.objects.first()
        self.assertEqual(new_explanation.explanation_text, 'A new explanation for an existing word')
        self.assertEqual(new_explanation.word, correct_word)


    def test_redirects_to_word_view(self):
        other_word = Word.objects.create()
        correct_word = Word.objects.create()

        response = self.client.post(
            '/%d/add_explanation' % (correct_word.id,),
            data={'explanation_input': 'A new item for an existing word'}
        )

        self.assertRedirects(response, '/%d/' % (correct_word.id,))

class SearchAndBrowseTest(TestCase):

    def test_uses_search_template(self):
        response = self.client.get('/search/byword')
        self.assertTemplateUsed(response, 'search.html')

    def test_render_after_POST(self):
        response = self.client.post('/search/byword', data={'search_input': 'A new list word'})
        self.assertEqual(response.status_code, 200)

    def test_return_correct_text(self):
        self.client.post('/add_word', data={'word_input': 'A new list word','explanation_input': 'yes it is'})
        response = self.client.post('/search/byword', data={'search_input': 'A new list word'})
        html = response.content.decode('utf8')
        self.assertIn('A new list word', html)
                
'''
class VoteTest(TestCase):
'''


