import string
import json

from urllib.parse import urlencode

from django import template

from CMS.enums import enums
from CMS.translations import DICT
from courses.models import STUDENT_SATISFACTION_KEY, ENTRY_INFO_KEY, AFTER_ONE_YEAR_KEY, AFTER_COURSE_KEY, \
    ACCREDITATION_KEY

register = template.Library()


@register.simple_tag
def queryparams(*_, **kwargs):
    safe_args = {key: value for key, value in kwargs.items() if value is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''


@register.simple_tag
def get_translation(*_, **kwargs):
    key = kwargs.get('key')
    language = kwargs.get('language')
    string = DICT.get(key).get(language) if key in DICT else ''

    if not string:
        string = DICT.get(key).get(enums.languages.ENGLISH) if key in DICT else ''

    if 'substitutions' in kwargs:
        string = string % kwargs.get('substitutions')
    return string


@register.simple_tag
def create_list(*args):
    return args


@register.simple_tag
def insert_values_to_rich_text(*_, **kwargs):
    list(kwargs.get('substitutions'))
    return kwargs.get('content').source % (kwargs.get('substitutions'))


@register.simple_tag
def length_of_list(view_list):
    return len(view_list)


@register.simple_tag
def map_distance_learning_values(key, language):
    if key in DICT.get('distance_learning_values'):
        return DICT.get('distance_learning_values').get(key).get(language)
    return key


@register.simple_tag
def should_show_accordion(courses, accordion_type):
    if accordion_type == STUDENT_SATISFACTION_KEY:
        if type(courses) == tuple:
            show = False
            for course in courses:
                if course.show_satisfaction_stats:
                    show = True
            return show
        return courses.show_satisfaction_stats
    elif accordion_type == ACCREDITATION_KEY:
        if type(courses) == tuple:
            show = False
            for course in courses:
                if course.accreditations:
                    show = True
            return show
        return courses.accreditations
    elif accordion_type == ENTRY_INFO_KEY:
        if type(courses) == tuple:
            show = False
            for course in courses:
                if course.show_entry_information_stats:
                    show = True
            return show
        return courses.show_entry_information_stats
    elif accordion_type == AFTER_ONE_YEAR_KEY:
        if type(courses) == tuple:
            show = False
            for course in courses:
                if course.show_after_one_year_stats:
                    show = True
            return show
        return courses.show_after_one_year_stats
    elif accordion_type == AFTER_COURSE_KEY:
        if type(courses) == tuple:
            show = False
            for course in courses:
                if course.show_after_course_stats:
                    show = True
            return show
        return courses.show_after_course_stats
    return False


@register.simple_tag
def title_to_id(title):
    return title.replace(' ', '_').lower()


@register.simple_tag
def get_alphabet():
    return list(string.ascii_lowercase)
