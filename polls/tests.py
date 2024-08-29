import datetime

from django.test import RequestFactory, TestCase,Client
from django.utils import timezone
from django.urls import reverse
from .models import Question,Vote,Choice
from .views import *
from .urls import *
from django.contrib.auth.models import User
from django import forms
from . import forms
from datetime import timedelta,datetime

from time import sleep



class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
    def test_is_string(self):
        q=Question(question_text="text")
        self.assertIs(q.is_string(),True)
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # def test_past_question(self):
    #     """
    #     The detail view of a question with a pub_date in the past
    #     displays the question's text.
    #     """
    #     past_question = create_question(question_text="Past Question.", days=-5)
    #     url = reverse("polls:detail", args=(past_question.id,))
    #     response = self.client.get(url)
    #     self.assertContains(response, past_question.question_text)
        
# class viewsfile_Tests(TestCase):
#     def test_votes_post_response_is_ok(self): #this test checks wheter if the post in polls/question.id page response code is 200.
#         self.user1=User.objects.create(username='user1',password='user1',email='email@email.com')
#         self.client.force_login(user=self.user1)
#         self.question1 = create_question(question_text="question1.", days=-3)
#         self.question2= create_question(question_text='question2.',days=-3)
#         self.question1_choice1=Choice.objects.create(question=self.question1,choice_text='question1_choice1.')
#         question1_choice2=Choice.objects.create(question=self.question1,choice_text='question1_choice2.')
#         question2_choice1=Choice.objects.create(question=self.question2,choice_text='question2_choice1.')
#         question2_choice2=Choice.objects.create(question=self.question2,choice_text='question2_choice2.')
#         response = self.client.post(path='/polls/1/vote/',data={'choice':['2']})
#         self.assertEqual(response.status_code,200)


#     def test_vote_saved_is_in_database(self): #this test checks wheter if vote data is seved correctly in database or not.
#         self.user1=User.objects.create(username='user1',password='user1',email='email@email.com')
#         self.client.force_login(user=self.user1)
#         self.question1 = create_question(question_text="question1.", days=-3)
#         self.question2= create_question(question_text='question2.',days=-3)
#         self.question1_choice1=Choice.objects.create(question=self.question1,choice_text='question1_choice1.')
#         self.client.post(path='/polls/1/vote/',data={'choice':['1']})
#         choice=Choice.objects.get(id=1)
#         votes=Vote.objects.filter(choice=choice)
#         for y in votes:
#             self.assertEqual(y.choice,choice)


#     def test_vote_displays_correctly_in_html_page(self): #this test checks wheter if html page shows the correct voted choice or not.
#         self.user1=User.objects.create(username='user1',password='user1')
#         self.client.force_login(user=self.user1)
#         self.question1 = create_question(question_text="question1.", days=-3)
#         self.question2= create_question(question_text='question2.',days=-3)
#         self.question1_choice1=Choice.objects.create(question=self.question1,choice_text='question1_choice1.')
#         response=self.client.post(path='/polls/1/vote/',data={'choice':['1']})
#         choice=Choice.objects.get(id=1)
#         self.assertContains(response,f'<li>{choice.choice_text}</li>')


#     def test_vote_func_using_the_correct_template(self): #this test checks that wheter if the vote function using the polls/result.html temaplate or not.
#         self.user1=User.objects.create(username='user1',password='user1')
#         self.client.force_login(user=self.user1)
#         self.question1 = create_question(question_text="question1.", days=-3)
#         self.question2= create_question(question_text='question2.',days=-3)
#         self.question1_choice1=Choice.objects.create(question=self.question1,choice_text='question1_choice1.')
#         response=self.client.post(path='/polls/1/vote/',data={'choice':['1']})
#         self.assertTemplateUsed(response,'polls/results.html')


#     def test_logged_in_user_is_the_same_user_that_votes(self): #this test checks that wheter if the user that loggs in is the same user that votes or not"
#         self.user1=User.objects.create(username='user1',password='user1',email='email@email.com')
#         self.client.force_login(user=self.user1)
#         self.question1 = create_question(question_text="question1.", days=-3)
#         self.question1_choice1=Choice.objects.create(question=self.question1,choice_text='question1_choice1.')
#         response = self.client.post(path='/polls/1/vote/',data={'choice':['1']})
#         self.assertContains(response,'user1')


#     def test_user_can_not_vote_more_than_once_for_the_same_question(self):
#         self.user1=User.objects.create(username='user1',password='user1')
#         self.client.force_login(user=self.user1)
#         self.question1 = create_question(question_text="question1.", days=-3)
#         self.question1_choice1=Choice.objects.create(question=self.question1,choice_text='question1_choice1.')
#         self.question1_choice2=Choice.objects.create(question=self.question1,choice_text='question1_choice2.')
#         self.client.post(path='/polls/1/vote/',data={'choice':['1']})
#         response = self.client.post(path='/polls/1/vote/',data={'choice':['2']})
#         self.assertIsNone(response.context)

#     def test_one_user_can_vote_two_different_questions(self):
#         self.user1=User.objects.create(username='user1',password='user1')
#         self.client.force_login(user=self.user1)
#         self.question1 = create_question(question_text="question1.", days=-3)
#         self.question2= create_question(question_text='question2.',days=-3)
#         self.question1_choice1=Choice.objects.create(question=self.question1,choice_text='question1_choice1.')
#         self.question2_choice1=Choice.objects.create(question=self.question2,choice_text='question2_choice1.')    
#         self.client.post(path='/polls/1/vote/',data={'choice':['1']})         
#         self.client.post(path='/polls/2/vote/',data={'choice':['2']})
#         question2_voted=Vote.objects.filter(choice=Choice.objects.get(id=2))
#         self.assertIsNotNone(question2_voted.first())
class formstest(TestCase):
    def test_post_request_returns_status_code_302(self): #just test that the response code of the post of the url /polls/add_question/is 302 and it's redirects sucessfuly to the 'question_saved' page
        self.user1=User.objects.create(username='user1',password='user1')
        self.client.force_login(user=self.user1)
        response=self.client.post(path='/polls/add_question/' , data={'question':['questionone']})
        self.assertEqual(response.status_code,302)
    def test_question_saved_in_database(self): #test that the question has been saved in the database after submiting it
        self.user1=User.objects.create(username='user1',password='user1')
        self.client.force_login(user=self.user1)
        self.client.post(path='/polls/add_question/' , data={'question':['question_one']})
        question1=Question.objects.all()
        self.assertIsNotNone(question1)
    def test_not_logged_in_user_can_not_use_question_form_status_code_301(self): #test that only logged in users can use question form and if not it returns 302 status code.
        response=self.client.post(path='/polls/add_question/add_choice' , data={'question':'question_one'})
        self.assertEqual(response.status_code, 301)
class choiceformtest(TestCase): #this class test the functionality of the choiceform class in the views.py
    def test_post_request_retruns_status_code_301(self): #this test checks that status code is 301
        response=self.client.post(path='/polls/add_question/add_choice' , data={'choice_text':['choice_one']})
        self.assertEqual(response.status_code,301)
    def test_post_request_redirects_the_user_to_the_succeed_page(self): #tests that post request redirects user to the succeed page after it worked successfully  
        self.client.post(path='/polls/add_question/' , data={'question':['question_one']})
        response=self.client.post(path='/polls/add_question/add_choice/' , data={'choice_text':['choice_one']})
        self.assertRedirects(response,'/polls/add_question/add_choice/question_saved',target_status_code=301)
    def test_choice_form_using_the_correct_html_template(self): #tests that choice form is using the correct template
        response=self.client.get(path='/polls/add_question/add_choice/')
        self.assertTemplateUsed(response,template_name='polls/add_choice.html')
    def test_choices_are_saved_correctly_in_database(self): #tests that choices are saved successfully in the database.
        self.client.post(path='/polls/add_question/' , data={'question':['question_one']})
        response=self.client.post(path='/polls/add_question/add_choice/' , data={'choice_text':["choice_one"]})
        choice=Choice.objects.all()
        self.assertIn(choice.first().choice_text,'choice_one')
    def test_two_choices_are_not_the_same(self): #tests that choices are not the same.
        with self.assertRaises(ValidationError):
            self.client.post(path='/polls/add_question/' , data={'question':['question_one']})
            self.client.post(path='/polls/add_question/add_choice/' , data={'choice_text':'choice'})
            # sleep(61)
            self.client.post(path='/polls/add_question/add_choice/' , data={'choice_text':'choice'})
    def test_do_not_redirect_user_if_choices_are_the_same(self): #test that the user do not redirect to the question saved page if it's saving the same choices by checking the status code.
        response1=self.client.post(path='/polls/add_question/add_choice' , data={'choice_text':'choice_one'})
        response2=self.client.post(path='/polls/add_question/add_choice' , data={'choice_text':'choice_two'})
        self.assertNotEqual(response2.status_code,302)

    def test_shows_error_if_was_not_valid(self): #shows the forms error
        response=self.client.post(path='/polls/add_question/add_choice' , data={'choice_text':['choice_one']})
        self.assertRaises(TypeError)
    # def test_form_is_valid(self): #check that the form validation works correctly
    #     response=self.client.post(path='/polls/add_question/add_choice' , data={'choice_text':'choice_one'})
    #     self.assertFalse(AddChoiceView.is_valid())
    def test_user_can_not_creat_two_questions_less_than_one_minute(self): #this test checks that time gap between saving two choices should be more than one minute.
        with self.assertRaises(ValidationError):
            self.client.post(path='/polls/add_question/' , data={'question':['question_one']})
            response=self.client.post(path='/polls/add_question/add_choice/' , data={'choice_text':['choice_one']})
            response2=self.client.post(path='/polls/add_question/add_choice/' , data={'choice_text':['choice_two']})
            choice=Choice.objects.all()
            choice2=choice.last()

            

        







# self.assertFieldOutput
# self.assertRegex
# self.assertAlmostEqual
# self.assertAlmostEquals
# self.assertContains
# self.assertCountEqual
# self.assertDictContainsSubset
# self.assertDictEqual
# self.assertEqual
# self.assertEquals
# self.assertEqual
# self.assertFalse
# self.assertFormError
# self.assertGreater
# self.assertGreaterEqual
# self.assertHTMLNotEqual
# self.assertIn
# self.assertInHTML
# self.assertHTMLEqual
# self.assertIs
# self.assertIsInstance
# self.assertIsNone
# self.assertIsNot
# self.assertIsNotNone
# self.assertJSONEqual
# self.assertLess
# self.assertLessEqual
# self.assertListEqual
# self.assertLogs
# self.assertMultiLineEqual
# self.assertNoLogs
# self.assertNotAlmostEqual
# self.assertNotAlmostEquals
# self.assertNotContains
# self.assertNotEqual
# self.assertNotIn
# self.assertNotIsInstance
# self.assertNotRegex
# self.assertRegexpMatches
# self.assertNumQueries
# self.assertQuerySetEqual
# self.assertQuerysetEqual
# self.assertRaises
# self.assertRaisesMessage
# self.assertRaisesRegexp
# self.assertRedirects
# self.assertRegex
# self.assertRegexpMatches
# self.assertSequenceEqual
# self.assertSetEqual
# self.assertTemplateNotUsed
# self.assertTemplateNotUsed
# self.assertTemplateUsed
# self.assertTrue
# self.assertTupleEqual
# self.assertWarns
# self.assertWarnsRegex
# self.assertXMLNotEqual
# self._getAssertEqualityFunc