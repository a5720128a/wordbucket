from datetime import datetime
from django.db import models
from django.utils import timezone

class Word(models.Model):
    #word (text)
    word = models.TextField(default='')
    date_pub = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.word
    def was_published_recently(self):
        return self.date_pub >= timezone.now() - datetime.timedelta(days=1)

class Explanation(models.Model):
    #foreign key
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    explanation_text = models.CharField(max_length=600)
    votes_like = models.IntegerField(default=0)
    votes_dislike = models.IntegerField(default=0)
    def __str__(self):
        return self.explanation_text
    def __int__(self):
        return self.votes_like
    def __int__(self):
        return self.votes_dislike

class Like(models.Model):
    #foreign key for Like and Dislike
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
    #user votes count
    user_like = models.TextField(default='')
    def __str__(self):
        return self.user_like

class Dislike(models.Model):
    #foreign key for Like and Dislike
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
    #user votes count
    user_dislike = models.TextField(default='')
    def __str__(self):
        return self.user_dislike
