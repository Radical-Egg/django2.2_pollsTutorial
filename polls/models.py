import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    g_question_text = models.CharField(max_length=200, verbose_name='Question')
    g_pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.g_question_text
    
    def was_published_recently(self):
        l_now = timezone.now()
        return l_now - datetime.timedelta(days=1) <= self.g_pub_date <= l_now

    # stuff for admin panel 
    was_published_recently.admin_order_field = 'g_pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    g_question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    g_choice_text = models.CharField(max_length=200, verbose_name='Choice Text')
    g_votes = models.IntegerField(default=0, verbose_name='Votes')

    def __str__(self):
        return self.g_choice_text