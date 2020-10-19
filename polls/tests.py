import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# class to test Question Model
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        l_time = timezone.now() + datetime.timedelta(days=30)
        l_future_question = Question(g_pub_date=l_time)
        self.assertIs(l_future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        l_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        l_old_question = Question(g_pub_date=l_time)
        self.assertIs(l_old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        l_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        l_recent_question = Question(g_pub_date=l_time)
        self.assertIs(l_recent_question.was_published_recently(), True)


# creating a test question
def create_question(p_question_text, p_days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    l_time = timezone.now() + datetime.timedelta(days=p_days)
    return Question.objects.create(g_question_text=p_question_text, g_pub_date=l_time)

# testing the  view

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        l_response = self.client.get(reverse('polls:index'))
        self.assertEqual(l_response.status_code, 200)
        self.assertContains(l_response, "No polls are available.")
        self.assertQuerysetEqual(l_response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(p_question_text="Past question.", p_days=-30)
        l_response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            l_response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(p_question_text="Future question.", p_days=30)
        l_response = self.client.get(reverse('polls:index'))
        self.assertContains(l_response, "No polls are available.")
        self.assertQuerysetEqual(l_response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(p_question_text="Past question.", p_days=-30)
        create_question(p_question_text="Future question.", p_days=30)
        l_response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            l_response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(p_question_text="Past question 1.", p_days=-30)
        create_question(p_question_text="Past question 2.", p_days=-5)
        l_response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            l_response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        l_future_question = create_question(p_question_text='Future question.', p_days=5)
        l_url = reverse('polls:detail', args=(l_future_question.id,))
        l_response = self.client.get(l_url)
        self.assertEqual(l_response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        l_past_question = create_question(p_question_text='Past Question.', p_days=-5)
        l_url = reverse('polls:detail', args=(l_past_question.id,))
        l_response = self.client.get(l_url)
        self.assertContains(l_response, l_past_question.g_question_text)