from django.contrib import admin


from .models import Word, Explanation, Like, Dislike

# Register your models here.

admin.site.register(Word)
admin.site.register(Explanation)
admin.site.register(Like)
admin.site.register(Dislike)
