from django.core import management
from django.test import TestCase, tag

from wagtail.core.models import Page

from courses.models import CourseManagePage

from django.conf import settings


@tag('github')
class CoursesTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        management.call_command('populate_cms')

    def test_front_page(self):

        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_LLB_LAW(self):

        response = self.client.get('http://localhost/course-details/10007804/U18-LAWLLB/Full-time/')
        self.assertEqual(200, response.status_code)
