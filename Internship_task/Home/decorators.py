from functools import wraps
from django.http.response import HttpResponse
from django.test.client import Client
from django.contrib.auth import get_user_model

User = get_user_model()

TEMPORARY_USER = {
  "username": "test_user_23589",
  "password": "test_password",
  "contact": "+917796845665"
}

def check_response(path='/', login_required=False, method="GET", post_data=None, expected=HttpResponse):
  """
  Quick test to check the correct response from views
  :param path: A web path to the desired page to test
  :type path: str

  :param login_required: Boolean to check if login is required
  :type login_required: bool

  :param method: Spacifies `HTTP` method for the test
  :type method: str

  :param post_data: Data to be posted with the `POST` method
  :type post_data: dict

  :param expected: Expected response for this path
  """

  post_data = post_data or dict()

  def wrapper(function):
    @wraps(function)
    def test(*args, client=Client(), **kwargs):
      if login_required:
        User.objects.create_user(**TEMPORARY_USER)
        client.login(**TEMPORARY_USER)

      if method == 'GET':
        response = client.get(path, follow=True)
      else:
        response = client.post(path, post_data)

      assert response.status_code == 200
      assert isinstance(response, expected)
      return function(*args, **kwargs)

    return test
  return wrapper
