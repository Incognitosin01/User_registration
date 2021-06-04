from django.test import TestCase
from .decorators import check_response
from django.utils.decorators import method_decorator
from django.urls import reverse

# Create your tests here.

class TestBasic(TestCase):

  @method_decorator(check_response(path=reverse('Home:login')))
  def test_login_page(self):
    # Add more tests here
    pass

  @method_decorator(check_response(path=reverse('Home:register')))
  def test_register_page(self):
    # add more tests here
    pass
  
  @method_decorator(check_response(path=reverse('Home:application'), login_required=True))
  def test_application_page(self):
    # add more tests here
    pass

  @method_decorator(check_response(path=reverse('Home:profile'), login_required=True))
  def test_profile_page(self):
    # add more tests here
    pass
