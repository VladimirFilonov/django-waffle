from django.contrib.auth.models import AnonymousUser

from test_utils import RequestFactory, TestCase

from test_app import views
from waffle.middleware import WaffleMiddleware


def get():
    request = RequestFactory().get('/foo')
    request.user = AnonymousUser()
    return request


def process_request(request, view):
    response = view(request)
    return WaffleMiddleware().process_response(request, response)


class WaffleTemplateTests(TestCase):
    def test_django_tags(self):
        request = get()
        response = process_request(request, views.flag_in_django)
        self.assertContains(response, 'flag off')
        self.assertContains(response, 'switch off')

    def test_jingo_tags(self):
        request = get()
        response = process_request(request, views.flag_in_jingo)
        self.assertContains(response, 'flag off')
        self.assertContains(response, 'switch off')
