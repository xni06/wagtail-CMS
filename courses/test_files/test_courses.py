from django.test import tag

from wagtail.core.models import Page

from core.tests import BaseTestCase
from courses.models import CourseManagePage

from django.conf import settings


@tag('github')
class CoursesTestCase(BaseTestCase):

    def test_front_page(self):

        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_LLB_LAW(self):

        print('---')
        print(settings.DATABASES['default'])
        print('---')

        page_count = Page.objects.count()

        print('+++')
        print(page_count)
        print('+++')

        response = self.client.get('http://localhost/course-details/10007804/U18-LAWLLB/Full-time/')
        self.assertEqual(200, response.status_code)
