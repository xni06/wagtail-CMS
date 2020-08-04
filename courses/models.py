from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.core import blocks

from CMS.translations import DICT
from CMS.enums import enums

from core.models import DiscoverUniBasePage
from core.utils import fallback_to
from courses import request_handler
from errors.models import ApiError
from institutions.models import InstitutionOverview
import datetime


STUDENT_SATISFACTION_KEY = 'student_satisfaction'
ENTRY_INFO_KEY = 'entry_information'
AFTER_ONE_YEAR_KEY = 'after_one_year'
EARNINGS_AFTER_COURSE_KEY = 'earnings_after_the_course'
EMPLOYMENT_AFTER_COURSE_KEY = 'employment_after_the_course'
ACCREDITATION_KEY = 'professional_accreditation'

# New accordion section ('Graduate Perceptions) added; various sections of this file are affected.
# TODO: In order for the new accordion section to be rendered in the UI, an instance of the corresponding
#   accordion panel must be created in the Wagtail admin site (http://0.0.0.0:8000/admin/);
#   go to Pages > Home > Course Details > 'ACCORDIONS' section > Add (+ icon) > add a panel of the new type.
#   Then Save Draft, then Publish.
GRADUATE_PERCEPTIONS_KEY = 'graduate_perceptions'
LINKS_TO_THE_INSTITUTION_WEBSITE_KEY = 'links_to_the_institution_website'


class AccordionPanel(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)


class SatisfactionDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return STUDENT_SATISFACTION_KEY


class EntryInfoDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return ENTRY_INFO_KEY


class AfterOneYearDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return AFTER_ONE_YEAR_KEY


class EarningsAfterCourseDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return EARNINGS_AFTER_COURSE_KEY


class EmploymentAfterCourseDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return EMPLOYMENT_AFTER_COURSE_KEY


class AccreditationDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return ACCREDITATION_KEY


class GraduatePerceptionsDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return GRADUATE_PERCEPTIONS_KEY


class LinksToTheInstitutionWebsiteDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return LINKS_TO_THE_INSTITUTION_WEBSITE_KEY


class SatisfactionBlock(AccordionPanel):
    lead_text = blocks.CharBlock(required=False)
    intro_body = blocks.RichTextBlock(blank=True)
    teaching_stats_header = blocks.CharBlock(required=False)
    learning_opportunities_stats_header = blocks.CharBlock(required=False)
    assessment_stats_header = blocks.CharBlock(required=False)
    support_stats_header = blocks.CharBlock(required=False)
    organisation_stats_header = blocks.CharBlock(required=False)
    learning_resources_stats_header = blocks.CharBlock(required=False)
    learning_community_stats_header = blocks.CharBlock(required=False)
    student_voice_stats_header = blocks.CharBlock(required=False)
    nhs_placement_stats_header = blocks.CharBlock(required=False)
    data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = SatisfactionDataSet


class EntryInformationBlock(AccordionPanel):
    qualification_heading = blocks.CharBlock(required=False)
    qualification_intro = blocks.CharBlock(required=False)
    qualification_label_explanation_heading = blocks.CharBlock(required=False)
    qualification_label_explanation_body = blocks.RichTextBlock(blank=True)
    qualification_data_source = blocks.RichTextBlock(blank=True)

    tariffs_heading = blocks.CharBlock(required=False)
    tariffs_intro = blocks.CharBlock(required=False)
    tariffs_data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = EntryInfoDataSet


class AfterOneYearBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)
    intro = blocks.CharBlock(required=False)
    lead = blocks.CharBlock(required=False)
    label_explanation_heading = blocks.CharBlock(required=False)
    label_explanation_body = blocks.RichTextBlock(blank=True)
    data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = AfterOneYearDataSet


class EarningsAfterCourseBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)
    intro = blocks.RichTextBlock(blank=True)

    average_earnings_inst_heading = blocks.RichTextBlock(blank=True)
    institution_graduates_heading = blocks.RichTextBlock(blank=True)

    after_fifteen_months_earnings_heading = blocks.CharBlock(required=False)
    after_fifteen_months_range_explanation = blocks.RichTextBlock(blank=True)
    after_fifteen_months_respondents_explanation = blocks.RichTextBlock(blank=True)
    after_fifteen_months_no_of_graduates_explanation = blocks.RichTextBlock(blank=True)
    after_fifteen_months_data_source = blocks.RichTextBlock(blank=True)

    after_three_years_earnings_heading = blocks.CharBlock(required=False)
    after_five_years_earnings_heading = blocks.CharBlock(required=False)
    after_three_five_years_data_source = blocks.RichTextBlock(blank=True)

    average_earnings_sector_heading = blocks.RichTextBlock(blank=True)
    respondents_live_in_explanation = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = EarningsAfterCourseDataSet


class EmploymentAfterCourseBlock(AccordionPanel):
    six_month_employment_lead = blocks.CharBlock(required=False)
    six_month_employment_data_source = blocks.RichTextBlock(blank=True)

    section_heading = blocks.RichTextBlock(required=False)
    intro = blocks.CharBlock(blank=True)

    six_month_employment_roles_heading = blocks.CharBlock(required=False)
    six_month_employment_roles_label_explanation_heading = blocks.CharBlock(required=False)
    six_month_employment_roles_data_source = blocks.RichTextBlock(blank=True)

    occupation_types_label_explanation_heading = blocks.CharBlock(required=False)
    occupation_types_label_explanation_body = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = EmploymentAfterCourseDataSet


class AccreditationBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)

    class Meta:
        value_class = AccreditationDataSet


class GraduatePerceptionsBlock(AccordionPanel):
    lead_text = blocks.CharBlock(required=False)
    intro_body = blocks.RichTextBlock(blank=True)

    perception_of_work_heading = blocks.CharBlock(required=False)
    data_source = blocks.RichTextBlock(blank=True)

    usefulness_explanation_heading = blocks.CharBlock(required=False)
    usefulness_explanation = blocks.RichTextBlock(blank=True)

    meaningfulness_explanation_heading = blocks.CharBlock(required=False)
    meaningfulness_explanation = blocks.RichTextBlock(blank=True)

    future_explanation_heading = blocks.CharBlock(required=False)
    future_explanation = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = GraduatePerceptionsDataSet


class LinksToTheInstitutionWebsiteBlock(AccordionPanel):
    course_information_on_website_header = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = LinksToTheInstitutionWebsiteDataSet


class CourseDetailPage(DiscoverUniBasePage):
    accordions = StreamField([
        ('satisfaction_panel', SatisfactionBlock(required=True, icon='collapse-down')),
        ('entry_information_panel', EntryInformationBlock(required=True, icon='collapse-down')),
        ('after_one_year_panel', AfterOneYearBlock(required=True, icon='collapse-down')),
        ('accreditation_panel', AccreditationBlock(required=True, icon='collapse-down')),
        ('earningsafter_course_panel', EarningsAfterCourseBlock(required=True, icon='collapse-down')),
        ('employment_after_course_panel', EmploymentAfterCourseBlock(required=True, icon='collapse-down')),
        ('graduate_perceptions_panel', GraduatePerceptionsBlock(required=True, icon='collapse-down')),
        ('links_to_the_institution_website_panel', LinksToTheInstitutionWebsiteBlock(required=True, icon='collapse-down'))
    ])
    uni_site_links_header = TextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        StreamFieldPanel('accordions'),
        FieldPanel('uni_site_links_header'),
    ]


class CourseComparisonPage(DiscoverUniBasePage):
    heading = TextField(blank=True)
    lead = TextField(blank=True)
    remove_text = RichTextField(blank=True)
    save_text = RichTextField(blank=True)
    compare_heading = TextField(blank=True)
    accordions = StreamField([
        ('satisfaction_panel', SatisfactionBlock(required=True, icon='collapse-down')),
        ('entry_information_panel', EntryInformationBlock(required=True, icon='collapse-down')),
        ('after_one_year_panel', AfterOneYearBlock(required=True, icon='collapse-down')),
        ('after_course_panel', EarningsAfterCourseBlock(required=True, icon='collapse-down')),
        ('accreditation_panel', AccreditationBlock(required=True, icon='collapse-down'))
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('lead'),
        FieldPanel('remove_text'),
        FieldPanel('save_text'),
        FieldPanel('compare_heading'),
        StreamFieldPanel('accordions'),
    ]


class CourseManagePage(DiscoverUniBasePage):
    heading = TextField(blank=True)
    lead = TextField(blank=True)
    save_text = RichTextField(blank=True)
    compare_text = RichTextField(blank=True)
    none_selected_text = RichTextField(blank=True)
    one_selected_text = RichTextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('lead'),
        FieldPanel('save_text'),
        FieldPanel('compare_text'),
        FieldPanel('none_selected_text'),
        FieldPanel('one_selected_text'),
    ]


class Course:
    MODES = {
        'Full-time': 1,
        'Part-time': 2,
        'FullTime': 1,
        'PartTime': 2,
        'Full time': 1,
        'Part time': 2
    }

    def __init__(self, data_obj, language):
        self.id = data_obj.get('id')
        self.display_language = language
        course_details = data_obj.get('course')
        if course_details:
            self.country = CourseCountry(course_details.get('country'))
            self.kis_course_id = course_details.get('kis_course_id')

            self.data_from_html = DICT.get('data_from_html').get(language)

            self.ucas_programme_id = course_details.get('ucas_programme_id')
            self.qualification = CourseQualification(course_details.get('qualification'))

            title = course_details.get('title')
            if title:
                self.english_title = fallback_to(title.get('english'), '')
                self.welsh_title = fallback_to(title.get('welsh'), '')
            self.honours_award_provision = course_details.get('honours_award_provision')

            self.institution = InstitutionOverview(course_details.get('institution'), language)
            self.locations = []
            if course_details.get('locations'):
                for location in course_details.get('locations'):
                    self.locations.append(CourseLocation(location, self.display_language))

            self.length = CourseLength(course_details.get('length_of_course'), language)
            self.mode = CourseMode(course_details.get('mode'))
            self.distance_learning = CourseDistanceLearning(course_details.get('distance_learning'),
                                                            self.display_language)
            self.sandwich_year = CourseSandwichYear(course_details.get('sandwich_year'))

            self.subject_names = []
            for subject in course_details.get('subjects'):
                self.subject_names.append(CourseSubject(subject, self.display_language))

            self.year_abroad = CourseYearAbroad(course_details.get('year_abroad'))
            self.foundation_year = CourseFoundationYear(course_details.get('foundation_year_availability'),
                                                        self.display_language)

            stats = course_details.get('statistics')
            if stats:
                self.satisfaction_stats = []
                for satisfaction_stats in stats.get('nss'):
                    self.satisfaction_stats.append(SatisfactionStatistics(satisfaction_stats, self.display_language))
                self.nhs_satisfaction_stats = []
                if stats.get('nhs_nss'):
                    for data_set in stats.get('nhs_nss'):
                        self.nhs_satisfaction_stats.append(SatisfactionStatistics(data_set, self.display_language))
                self.entry_stats = []
                for data_set in stats.get('entry'):
                    self.entry_stats.append(EntryStatistics(data_set, self.display_language))
                self.tariff_stats = []
                for data_set in stats.get('tariff'):
                    self.tariff_stats.append(TariffStatistics(data_set, self.display_language))
                self.continuation_stats = []
                for data_set in stats.get('continuation'):
                    self.continuation_stats.append(ContinuationStatistics(data_set, self.display_language))
                self.salary_stats = []
                for data_set in stats.get('salary'):
                    self.salary_stats.append(SalaryStatistics(data_set, self.display_language, title))
                self.leo_stats = []
                for data_set in stats.get('leo'):
                    self.leo_stats.append(LEOStatistics(data_set, self.display_language))
                self.employment_stats = []
                for data_set in stats.get('employment'):
                    self.employment_stats.append(EmploymentStatistics(data_set, self.display_language))
                self.job_type_stats = []
                for data_set in stats.get('job_type'):
                    self.job_type_stats.append(JobTypeStatistics(data_set, self.display_language))
                self.job_lists = []
                for data_set in stats.get('job_list'):
                    self.job_lists.append(JobList(data_set, self.display_language))

            self.accreditations = []
            accreditations = course_details.get('accreditations')
            if accreditations:
                for accreditation in accreditations:
                    self.accreditations.append(CourseAccreditation(accreditation, self.display_language))

            self.course_links = self.set_course_links(course_details.get('links'), self.display_language)
            self.overall_satisfaction = self.sync_satisfaction_stats()

            self.in_employment_15_mths = course_details.get('in_employment_15_mths')

            self.graduate_perceptions = []
            for data_set in course_details.get('go_voice_work'):
                self.graduate_perceptions.append(GraduatePerceptionStatistics(data_set, self.display_language))

            self.summary_med_sal_value = "no_data"
            self.summary_med_sal_text_trans_key = "no_data"

            current_year = datetime.datetime.now().year
            self.go_year_range = "{}-{}".format(current_year-2, current_year-1)
            self.leo3_year_range = "{}-{}".format(current_year-4, current_year-3)
            self.leo5_year_range = "{}-{}".format(current_year-6, current_year-5)

            self.salaries_inst = []
            if course_details.get('go_salary_inst'):
                self.salaries_inst.append(Salary(course_details.get('go_salary_inst'), self.display_language))
                self.summary_med_sal_value = Salary(course_details.get('go_salary_inst'), self.display_language).med
                self.summary_med_sal_text_trans_key = "average_earnings_course_overview_2a"
            if course_details.get('leo3_inst'):
                self.salaries_inst.append(Salary(course_details.get('leo3_inst'), self.display_language))
                if self.summary_med_sal_value == "no_data":
                    self.summary_med_sal_value = Salary(course_details.get('leo3_inst'), self.display_language).med
                    self.summary_med_sal_text_trans_key = "average_earnings_course_overview_2b"
            if course_details.get('leo5_inst'):
                self.salaries_inst.append(Salary(course_details.get('leo5_inst'), self.display_language))

            self.salaries_sector = []
            if course_details.get('go_salary_sector'):
                self.salaries_sector.append(SectorSalary(course_details.get('go_salary_sector'), self.display_language))
            if course_details.get('leo3_salary_sector'):
                self.salaries_sector.append(SectorSalary(course_details.get('leo3_salary_sector'), self.display_language))
            if course_details.get('leo5_salary_sector'):
                self.salaries_sector.append(SectorSalary(course_details.get('leo5_salary_sector'), self.display_language))


    def set_course_links(self, links, language):
        link_objs = {'course_details': [], 'costs_support': []}
        if enums.uni_link_keys.COURSE in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.COURSE).get(language),
                                                   links.get(enums.uni_link_keys.COURSE),
                                                   enums.languages_map.get(language)))
        if enums.uni_link_keys.TEACHING_METHODS in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.TEACHING_METHODS).get(language),
                                        links.get(enums.uni_link_keys.TEACHING_METHODS),
                                        enums.languages_map.get(language)))
        if enums.uni_link_keys.ASSESSMENT in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.ASSESSMENT).get(language),
                                                   links.get(enums.uni_link_keys.ASSESSMENT),
                                                   enums.languages_map.get(language)))
        if enums.uni_link_keys.EMPLOYMENT in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.EMPLOYMENT).get(language),
                                                   links.get(enums.uni_link_keys.EMPLOYMENT),
                                                   enums.languages_map.get(language)))
        if enums.uni_link_keys.COSTS in links:
            link_objs.get('costs_support').append(CourseLink(DICT.get(enums.uni_link_keys.COSTS).get(language),
                                                  links.get(enums.uni_link_keys.COSTS),
                                                  enums.languages_map.get(language)))
        if self.locations and self.locations[0].links and enums.uni_link_keys.ACCOMMODATION in self.locations[0].links:
            link_objs.get('costs_support').append(CourseLink(DICT.get(enums.uni_link_keys.ACCOMMODATION).get(language),
                                                  self.locations[0].links.get(enums.uni_link_keys.ACCOMMODATION),
                                                  enums.languages_map.get(language)))
        if enums.uni_link_keys.FINANCIAL_SUPPORT in links:
            link_objs.get('costs_support').append(CourseLink(DICT.get(enums.uni_link_keys.FINANCIAL_SUPPORT).get(language),
                                                  links.get(enums.uni_link_keys.FINANCIAL_SUPPORT),
                                                  enums.languages_map.get(language)))
        return link_objs

    @property
    def number_of_locations(self):
        return len(self.locations)

    @property
    def locations_list(self):
        location_names = []
        for location in self.locations:
            location_names.append(location.english_name)
        return ', '.join(location_names)

    @property
    def show_satisfaction_stats(self):
        show_satisfaction_stats = self.satisfaction_stats and self.satisfaction_stats[0].show_satisfaction_stats()
        show_nhs_stats = self.nhs_satisfaction_stats and self.nhs_satisfaction_stats[0].show_nhs_stats()
        return show_satisfaction_stats or show_nhs_stats

    @property
    def has_multiple_satisfaction_stats(self):
        return len(self.overall_satisfaction) > 1

    @property
    def show_entry_information_stats(self):
        show_entry_stats = self.entry_stats and self.entry_stats[0].display_stats
        show_tariff_stats = self.tariff_stats and self.tariff_stats[0].show_stats()

        return show_entry_stats or show_tariff_stats

    @property
    def has_multiple_entry_stats(self):
        return len(self.entry_stats) > 1

    @property
    def has_multiple_tariff_stats(self):
        return len(self.tariff_stats) > 1

    @property
    def show_after_one_year_stats(self):
        return self.continuation_stats and self.continuation_stats[0].display_stats

    @property
    def has_multiple_one_year_stats(self):
        return len(self.continuation_stats) > 1

    @property
    def has_multiple_graduate_perceptions_stats(self):
        return len(self.graduate_perceptions) > 1

    @property
    def show_after_course_stats(self):
        show_salary_stats = self.salary_stats and self.salary_stats[0].display_stats
        show_employment_stats = self.employment_stats and self.employment_stats[0].display_stats
        show_job_type_stats = self.job_type_stats and self.job_type_stats[0].display_stats
        show_job_lists = self.job_lists and self.job_lists[0].show_stats
        return show_employment_stats or show_job_type_stats or show_salary_stats or self.show_leo or show_job_lists

    @property
    def show_salary_lead(self):
        show_salary_stats = self.salary_stats and self.salary_stats[0].display_stats
        return show_salary_stats or self.show_leo

    @property
    def has_multiple_salary_stats(self):
        return len(self.salary_stats) > 1

    @property
    def has_multiple_leo_stats(self):
        return len(self.leo_stats) > 1

    @property
    def has_multiple_employment_stats(self):
        return len(self.employment_stats) > 1

    @property
    def has_multiple_job_type_stats(self):
        return len(self.job_type_stats) > 1

    @property
    def has_multiple_job_lists(self):
        return len(self.job_lists) > 1

    @property
    def show_leo(self):
        return self.is_in_england and self.leo_stats and self.leo_stats[0].display_stats

    @property
    def is_in_england(self):
        return self.country.name == 'England'

    def display_title(self):
        honours = ""
        if int(self.honours_award_provision) == 1:
            honours = "(Hons) "

        english_title = self.qualification.label + " " + honours + self.english_title
        welsh_title = self.qualification.label + " " + honours + self.welsh_title

        if self.display_language == enums.languages.ENGLISH:
            return english_title if self.english_title else welsh_title
        return welsh_title if self.welsh_title else english_title

    @classmethod
    def find(cls, institution_id, course_id, mode, language):
        course = None
        error = None

        response = request_handler.load_course_data(institution_id, course_id, cls.get_mode_code(mode))

        if response.ok:
            course = cls(response.json(), language)
        else:
            error = ApiError(response.status_code, 'Loading details for course %s %s at %s' %
                             (course_id, mode, institution_id))

        return course, error

    @staticmethod
    def get_mode_code(mode):
        return Course.MODES.get(mode)

    def sync_satisfaction_stats(self):
        overall_satisfaction = []
        for satisfaction_stats in self.satisfaction_stats:
            satisfaction_pair = {'satisfaction_stats': satisfaction_stats, 'nhs_satisfaction_stats': None}
            for nhs_stats in self.nhs_satisfaction_stats:
                if nhs_stats.subject_code == satisfaction_stats.subject_code:
                    satisfaction_pair['nhs_satisfaction_stats'] = nhs_stats
            overall_satisfaction.append(satisfaction_pair)
        return overall_satisfaction


class CourseCountry:

    def __init__(self, data_obj):
        if data_obj:
            self.name = fallback_to(data_obj.get('name'), '')
            self.code = data_obj.get('code')


class CourseDistanceLearning:

    def __init__(self, data_obj, language):
        self.display_language = language
        if data_obj:
            self.code = str(data_obj.get('code'))
            self.label = fallback_to(data_obj.get('label'), '')

    def display_label(self):
        if self.code is not None and self.code in DICT.get('distance_learning_values'):
            return DICT.get('distance_learning_values').get(self.code).get(self.display_language)
        return DICT.get('unknown').get(self.display_language)


class CourseFoundationYear:

    def __init__(self, data_obj, language):
        self.label = DICT.get('unknown').get(language)
        if data_obj:
            self.code = data_obj.get('code')
            self.label = fallback_to(data_obj.get('label'), '')


class CourseLength:

    def __init__(self, data_obj, language):
        self.label = 0
        if data_obj:
            self.code = data_obj.get('code')
            self.label = fallback_to(data_obj.get('label'), '')


class CourseLink:

    def __init__(self, name, link_obj, language_key):
        self.label = name
        if language_key in link_obj:
            self.link = link_obj.get(language_key)
        else:
            self.link = fallback_to(link_obj.get(enums.languages_full.ENGLISH), '')


class CourseLocation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.latitude = data_obj.get('latitude')
        self.longitude = data_obj.get('longitude')
        name = data_obj.get('name')
        if name:
            self.english_name = fallback_to(name.get('english'), '')
            self.welsh_name = fallback_to(name.get('welsh'), '')
        self.links = data_obj.get('links')

    def display_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.english_name if self.english_name else self.welsh_name
        else:
            return self.welsh_name if self.welsh_name else self.english_name


class CourseMode:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseQualification:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseSandwichYear:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseYearAbroad:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseSubject:
    def __init__(self, data_obj, language):
        self.display_language = language
        self.subject_english = data_obj.get('english', '')
        self.subject_welsh = data_obj.get('welsh', '')

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english


class EntryStatistics:

    def __init__(self, data_obj, display_language):
        self.display_language = display_language
        self.display_stats = False
        self.aggregation_level = 0
        self.number_of_students = 0
        self.a_level = 0
        self.access = 0
        self.another_higher_education_qualifications = 0
        self.baccalaureate = 0
        self.degree = 0
        self.foundation = 0
        self.none = 0
        self.other_qualifications = 0
        self.unavailable_code = ''
        self.unavailable_reason = ''

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['a-level', 'access',
                                                                 'another_higher_education_qualifications',
                                                                 'baccalaureate', 'degree', 'foundation', 'none',
                                                                 'other_qualifications', 'number_of_students'])

            self.aggregation_level = fallback_to(data_obj.get('aggregation_level'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)

            self.a_level = fallback_to(data_obj.get('a-level'), 0)
            self.access = fallback_to(data_obj.get('access'), 0)
            self.another_higher_education_qualifications = fallback_to(
                data_obj.get('another_higher_education_qualifications'), 0)
            self.baccalaureate = fallback_to(data_obj.get('baccalaureate'), 0)
            self.degree = fallback_to(data_obj.get('degree'), 0)
            self.foundation = fallback_to(data_obj.get('foundation'), 0)
            self.none = fallback_to(data_obj.get('none'), 0)
            self.other_qualifications = fallback_to(data_obj.get('other_qualifications'), 0)

            subject_data = data_obj.get('subject')
            if subject_data:
                self.subject_code = subject_data.get('code')
                self.subject_english = subject_data.get('english_label')
                self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    # TODO refactor all these same functions to a shared one
    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class ContinuationStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.display_stats = False
        self.dormant = 0
        self.continuing = 0
        self.gained = 0
        self.left = 0
        self.lower = 0
        self.number_of_students = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['dormant', 'continuing_with_provider', 'gained',
                                                                 'left', 'lower'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)

            self.dormant = fallback_to(data_obj.get('dormant'), 0)
            self.continuing = fallback_to(data_obj.get('continuing_with_provider'), 0)
            self.gained = fallback_to(data_obj.get('gained'), 0)
            self.left = fallback_to(data_obj.get('left'), 0)
            self.lower = fallback_to(data_obj.get('lower'), 0)

            subject_data = data_obj.get('subject')
            if subject_data:
                self.subject_code = subject_data.get('code')
                self.subject_english = subject_data.get('english_label')
                self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    @property
    def continuing_or_complete(self):
        return self.continuing + self.gained

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english
        
        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class EmploymentStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.display_stats = False
        self.aggregation_level = 0
        self.unemp_not_work_since_grad = 0
        self.doing_further_study = 0
        self.in_work = 0
        self.in_work_and_study = 0
        self.unemp_prev_emp_since_grad = 0
        self.other = 0
        self.number_of_students = 0
        self.response_rate = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['unemp_not_work_since_grad', 'doing_further_study', 'in_work',
                                                                 'in_work_and_study', 'unemp_prev_emp_since_grad',
                                                                 'other',
                                                                 'number_of_students', 'response_rate'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.unemp_not_work_since_grad = fallback_to(data_obj.get('unemp_not_work_since_grad'), 0)
            self.doing_further_study = fallback_to(data_obj.get('doing_further_study'), 0)
            self.in_work = fallback_to(data_obj.get('in_work'), 0)
            self.in_work_and_study = fallback_to(data_obj.get('in_work_and_study'), 0)
            self.unemp_prev_emp_since_grad = fallback_to(data_obj.get('unemp_prev_emp_since_grad'), 0)
            self.other = fallback_to(data_obj.get('other'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)
            self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'

            subject_data = data_obj.get('subject')
            if subject_data:
                self.subject_code = subject_data.get('code')
                self.subject_english = subject_data.get('english_label')
                self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    @property
    def work_and_or_study(self):
        return self.unemp_prev_emp_since_grad

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class JobTypeStatistics:

    def __init__(self, data_obj, language):
        self.display_stats = False
        self.display_language = language
        self.aggregation_level = 0
        self.non_professional_or_managerial_jobs = 0
        self.professional_or_managerial_jobs = 0
        self.unknown_professions = 0
        self.number_of_students = 0
        self.response_rate = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['non_professional_or_managerial_jobs',
                                                                 'professional_or_managerial_jobs', 'response_rate',
                                                                 'unknown_professions', 'number_of_students'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.non_professional_or_managerial_jobs = fallback_to(data_obj.get('non_professional_or_managerial_jobs'),
                                                                   0)
            self.professional_or_managerial_jobs = fallback_to(data_obj.get('professional_or_managerial_jobs'), 0)
            self.unknown_professions = fallback_to(data_obj.get('unknown_professions'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)
            self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'

            subject_data = data_obj.get('subject')
            if subject_data:
                self.subject_code = subject_data.get('code')
                self.subject_english = subject_data.get('english_label')
                self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class SalaryStatistics:

    def __init__(self, data_obj, language, course_title):
        self.display_stats = False
        self.display_language = language
        self.aggregation_level = 0
        self.higher_quartile = 0
        self.lower_quartile = 0
        self.median = 0
        self.sector_higher_quartile = 0
        self.sector_lower_quartile = 0
        self.sector_median = 0
        self.number_of_students = 0
        self.response_rate = 0
        self.subject_english_label = ''
        self.subject_welsh_label = ''

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['higher_quartile', 'lower_quartile', 'median',
                                                                 'sector_higher_quartile', 'sector_lower_quartile',
                                                                 'sector_median', 'number_of_graduates',
                                                                 'response_rate'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.higher_quartile = fallback_to(data_obj.get('higher_quartile'), 0)
            self.lower_quartile = fallback_to(data_obj.get('lower_quartile'), 0)
            self.median = fallback_to(data_obj.get('median'), 0)
            self.sector_higher_quartile = fallback_to(data_obj.get('sector_higher_quartile'), 0)
            self.sector_lower_quartile = fallback_to(data_obj.get('sector_lower_quartile'), 0)
            self.sector_median = fallback_to(data_obj.get('sector_median'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_graduates'), 0)
            self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'

            subject = data_obj.get('subject')
            if subject:
                self.subject_code = subject.get('code')
                self.subject_english_label = fallback_to(subject.get("english_label"), '')
                self.subject_welsh_label = fallback_to(subject.get("welsh_label"), '')
            elif course_title:
                self.subject_english_label = fallback_to(course_title.get("english"), '')
                self.subject_welsh_label = fallback_to(course_title.get("welsh"), '')
            else:
                self.subject_english_label = ''
                self.subject_welsh_label = ''

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    def display_subject_label(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english_label if self.subject_english_label else self.subject_welsh_label
        return self.subject_welsh_label if self.subject_welsh_label else self.subject_english_label

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class LEOStatistics:

    def __init__(self, data_obj, language):
        self.display_stats = False
        self.display_language = language
        self.subject_english_label = ''
        self.subject_welsh_label = ''
        self.aggregation_level = 0
        self.higher_quartile = 0
        self.lower_quartile = 0
        self.median = 0
        self.number_of_graduates = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ["aggregation_level", "higher_quartile",
                                                                 "lower_quartile", "median", "number_of_graduates"])

            self.aggregation_level = data_obj.get("aggregation_level")
            self.higher_quartile = fallback_to(data_obj.get("higher_quartile"), 0)
            self.lower_quartile = fallback_to(data_obj.get("lower_quartile"), 0)
            self.median = fallback_to(data_obj.get("median"), 0)
            self.number_of_graduates = fallback_to(data_obj.get("number_of_graduates"), 0)

            subject = data_obj.get('subject')
            if subject:
                self.subject_code = subject.get('code')
                self.subject_english_label = fallback_to(subject.get("english_label"), '')
                self.subject_welsh_label = fallback_to(subject.get("welsh_label"), '')

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    def display_subject_label(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english_label if self.subject_english_label else self.subject_welsh_label
        return self.subject_welsh_label if self.subject_welsh_label else self.subject_english_label

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class SatisfactionStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.aggregation_level = data_obj.get('aggregation_level')
        self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)
        self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'
        self.question_1 = SatisfactionQuestion(data_obj.get('question_1'))
        self.question_2 = SatisfactionQuestion(data_obj.get('question_2'))
        self.question_3 = SatisfactionQuestion(data_obj.get('question_3'))
        self.question_4 = SatisfactionQuestion(data_obj.get('question_4'))
        self.question_5 = SatisfactionQuestion(data_obj.get('question_5'))
        self.question_6 = SatisfactionQuestion(data_obj.get('question_6'))
        self.question_7 = SatisfactionQuestion(data_obj.get('question_7'))
        self.question_8 = SatisfactionQuestion(data_obj.get('question_8'))
        self.question_9 = SatisfactionQuestion(data_obj.get('question_9'))
        self.question_10 = SatisfactionQuestion(data_obj.get('question_10'))
        self.question_11 = SatisfactionQuestion(data_obj.get('question_11'))
        self.question_12 = SatisfactionQuestion(data_obj.get('question_12'))
        self.question_13 = SatisfactionQuestion(data_obj.get('question_13'))
        self.question_14 = SatisfactionQuestion(data_obj.get('question_14'))
        self.question_15 = SatisfactionQuestion(data_obj.get('question_15'))
        self.question_16 = SatisfactionQuestion(data_obj.get('question_16'))
        self.question_17 = SatisfactionQuestion(data_obj.get('question_17'))
        self.question_18 = SatisfactionQuestion(data_obj.get('question_18'))
        self.question_19 = SatisfactionQuestion(data_obj.get('question_19'))
        self.question_20 = SatisfactionQuestion(data_obj.get('question_20'))
        self.question_21 = SatisfactionQuestion(data_obj.get('question_21'))
        self.question_22 = SatisfactionQuestion(data_obj.get('question_22'))
        self.question_23 = SatisfactionQuestion(data_obj.get('question_23'))
        self.question_24 = SatisfactionQuestion(data_obj.get('question_24'))
        self.question_25 = SatisfactionQuestion(data_obj.get('question_25'))
        self.question_26 = SatisfactionQuestion(data_obj.get('question_26'))
        self.question_27 = SatisfactionQuestion(data_obj.get('question_27'))

        subject_data = fallback_to(data_obj.get('subject'), {})
        self.subject_code = subject_data.get('code', '')
        self.subject_english = subject_data.get('english_label', '')
        self.subject_welsh = subject_data.get('welsh_label', '')

        unavailable_data = fallback_to(data_obj.get('unavailable'), {})
        self.unavailable_code = unavailable_data.get('code')
        self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
        self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
        self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
        self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
        self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
        self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
        self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    def show_teaching_stats(self):
        return self.question_1.show_data_point or self.question_2.show_data_point or \
               self.question_3.show_data_point or self.question_4.show_data_point

    def show_learning_opps_stats(self):
        return self.question_5.show_data_point or self.question_6.show_data_point or \
               self.question_7.show_data_point

    def show_assessment_stats(self):
        return self.question_8.show_data_point or self.question_9.show_data_point or \
               self.question_10.show_data_point or self.question_11.show_data_point

    def show_support_stats(self):
        return self.question_12.show_data_point or self.question_13.show_data_point or \
               self.question_14.show_data_point

    def show_organisation_stats(self):
        return self.question_15.show_data_point or self.question_16.show_data_point or \
               self.question_17.show_data_point

    def show_learning_resources_stats(self):
        return self.question_18.show_data_point or self.question_19.show_data_point or \
               self.question_20.show_data_point

    def show_learning_community_stats(self):
        return self.question_21.show_data_point or self.question_22.show_data_point

    def show_voice_stats(self):
        return self.question_23.show_data_point or self.question_24.show_data_point or \
               self.question_25.show_data_point or self.question_26.show_data_point

    def show_satisfaction_stats(self):
        return self.show_teaching_stats() or self.show_learning_opps_stats() or self.show_assessment_stats() or \
               self.show_organisation_stats() or self.show_learning_resources_stats() or \
               self.show_learning_community_stats() or self.show_voice_stats()

    def show_nhs_stats(self):
        return self.question_1.show_data_point or self.question_2.show_data_point or \
               self.question_3.show_data_point or self.question_4.show_data_point or \
               self.question_5.show_data_point or self.question_6.show_data_point

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class SatisfactionQuestion:

    def __init__(self, question_data):
        self.show_data_point = False
        if question_data:
            self.show_data_point = 'agree_or_strongly_agree' in question_data
            self.description = fallback_to(question_data.get('description'), '')
            self.agree_or_strongly_agree = fallback_to(question_data.get('agree_or_strongly_agree'), 0)


class TariffStatistics:

    def __init__(self, tariff_data, display_language):
        self.display_language = display_language
        self.tariffs = []

        if tariff_data:
            self.aggregation = tariff_data.get('aggregation')
            self.number_of_students = fallback_to(tariff_data.get('number_of_students'), 0)
            if tariff_data.get('tariffs'):
                for tariff in tariff_data.get('tariffs'):
                    self.tariffs.append(Tariff(tariff))
            self.tariffs.reverse()

            subject_data = tariff_data.get('subject')
            if subject_data:
                self.subject_code = subject_data.get('code')
                self.subject_english = subject_data.get('english_label')
                self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = fallback_to(tariff_data.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

    def show_stats(self):
        return self.tariffs

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class Tariff:
    LABELS = {
        "T001": "< 48",
        "T048": "48 - 63",
        "T064": "64 - 79",
        "T080": "80 - 95",
        "T096": "96 - 111",
        "T112": "112 - 127",
        "T128": "128 - 143",
        "T144": "144 - 159",
        "T160": "160 - 175",
        "T176": "176 - 191",
        "T192": "192 - 207",
        "T208": "208 - 223",
        "T224": "224 - 239",
        "T240": "240 <",
    }

    def __init__(self, tariff):
        self.code = tariff.get('code')
        self.description = fallback_to(tariff.get('description'), '')
        self.entrants = fallback_to(tariff.get('entrants'), 0)

    @property
    def label(self):
        if self.code:
            return self.LABELS[self.code]
        return ''


class CourseAccreditation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.type = fallback_to(data_obj.get("type"), '')
        self.accreditor_url = fallback_to(data_obj.get('accreditor_url'), '')
        text = data_obj.get('text')
        if text:
            self.text_english = fallback_to(text.get('english'), '')
            self.text_welsh = fallback_to(text.get('welsh'), '')

        url = data_obj.get('url')
        self.url_english = ''
        self.url_welsh = ''
        if url:
            self.url_english = fallback_to(url.get('english'), '')
            self.url_welsh = fallback_to(url.get('welsh'), '')

        dependent = data_obj.get('dependent_on')
        if dependent:
            self.dependent_on_code = dependent.get('code')
            self.dependent_on_label = fallback_to(dependent.get('label'), '')

    def display_text(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.text_english if self.text_english else self.text_welsh
        return self.text_welsh if self.text_welsh else self.text_english

    def language_url(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.url_english if self.url_english else self.url_welsh
        return self.url_welsh if self.url_welsh else self.url_english

    def show_dependency(self):
        return self.dependent_on_code == '1'


class JobList:

    def __init__(self, jobs_data, display_language):
        self.display_language = display_language
        self.jobs = []

        if jobs_data:
            self.aggregation = jobs_data.get('aggregation')
            self.number_of_students = fallback_to(jobs_data.get('number_of_students'), 0)
            self.response_rate = str(fallback_to(jobs_data.get('response_rate'), 0)) + '%'

            subject_data = fallback_to(jobs_data.get('subject'), {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label', '')
            self.subject_welsh = subject_data.get('welsh_label', '')

            unavailable_data = fallback_to(jobs_data.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')

            if jobs_data.get('list'):
                for job in jobs_data.get('list'):
                    self.jobs.append(Job(job, self.display_language))

    def show_stats(self):
        return self.jobs

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable["find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class Job:

    def __init__(self, job_data, display_language):
        self.display_language = display_language
        if job_data:
            self.job = fallback_to(job_data.get('job'), '')
            self.percentage = fallback_to(job_data.get('percentage_of_students'),0)
            self.order = job_data.get('order')
            self.hss = job_data.get('hss')


class GraduatePerceptionStatistics:

    def __init__(self, go_voice_work_data, display_language):
        self.display_language = display_language

        subject_data = fallback_to(go_voice_work_data.get('subject'), {})
        self.subject_code = subject_data.get('code', '')
        self.subject_english = subject_data.get('english_label', '')
        self.subject_welsh = subject_data.get('welsh_label', '')

        if go_voice_work_data:
            self.go_work_skills = go_voice_work_data['go_work_skills']
            self.go_work_mean = go_voice_work_data['go_work_mean']
            self.go_work_on_track = go_voice_work_data['go_work_on_track']
            self.go_work_pop = go_voice_work_data['go_work_pop']
            self.go_work_resp_rate = go_voice_work_data['go_work_resp_rate']

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english


class Salary:

    def __init__(self, salary_data, display_language):
        self.display_language = display_language
        if salary_data:
            self.pop = salary_data['pop']
            self.resp_rate = salary_data['resp_rate']
            self.lq = salary_data['lq']
            self.med = salary_data['med']
            self.uq = salary_data['uq']

            self.unavail_reason = salary_data['unavail_reason']
            self.aggregate = salary_data['agg']
            #self.unavail_text_english = salary_data['unavail_text_english']
            #self.unavail_text_welsh = salary_data['unavail_text_welsh']

            self.unavailable_reason = "" #fallback_to(salary_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(salary_data['unavail_text_english'], '')
            self.unavailable_reason_welsh = fallback_to(salary_data['unavail_text_welsh'], '')
            # self.unavailable_url_english = fallback_to(salary_data.get('url_english'), '')
            # self.unavailable_url_welsh = fallback_to(salary_data.get('url_welsh'), '')

            if 'inst_prov_pc_uk' in salary_data:
                self.prov_pc_uk = salary_data['inst_prov_pc_uk']
                self.prov_pc_e = salary_data['inst_prov_pc_e']
                self.prov_pc_s = salary_data['inst_prov_pc_s']
                self.prov_pc_w = salary_data['inst_prov_pc_w']
                self.prov_pc_ni = salary_data['inst_prov_pc_ni']
                self.prov_pc_nw = salary_data['inst_prov_pc_nw']
                self.prov_pc_ne = salary_data['inst_prov_pc_ne']
                self.prov_pc_em = salary_data['inst_prov_pc_em']
                self.prov_pc_wm = salary_data['inst_prov_pc_wm']
                self.prov_pc_ee = salary_data['inst_prov_pc_ee']
                self.prov_pc_se = salary_data['inst_prov_pc_se']
                self.prov_pc_sw = salary_data['inst_prov_pc_sw']
                self.prov_pc_yh = salary_data['inst_prov_pc_yh']
                self.prov_pc_lo = salary_data['inst_prov_pc_lo']
                self.prov_pc_ed = salary_data['inst_prov_pc_ed']
                self.prov_pc_gl = salary_data['inst_prov_pc_gl']
                self.prov_pc_cf = salary_data['inst_prov_pc_cf']

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable["reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        # if self.display_language == enums.languages.ENGLISH:
        #     unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
        #         else self.unavailable_url_welsh
        # else:
        #     unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable


class SectorSalary:

    def __init__(self, salary_data, display_language):
        self.display_language = display_language
        self.no_salary_node = "true"

        if salary_data:
            self.no_salary_node = "false"
            self.unavail_reason = salary_data['unavail_reason']
            self.lq_uk = salary_data['lq_uk']
            self.med_uk = salary_data['med_uk']
            self.uq_uk = salary_data['uq_uk']
            self.pop_uk = salary_data['pop_uk']
            self.resp_uk = salary_data['resp_uk']

            self.lq_e = salary_data['lq_e']
            self.med_e = salary_data['med_e']
            self.uq_e = salary_data['uq_e']
            self.pop_e = salary_data['pop_e']
            self.resp_e = salary_data['resp_e']

            self.lq_w = salary_data['lq_w']
            self.med_w = salary_data['med_w']
            self.uq_w = salary_data['uq_w']
            self.pop_w = salary_data['pop_w']
            self.resp_w = salary_data['resp_w']

            self.lq_s = salary_data['lq_s']
            self.med_s = salary_data['med_s']
            self.uq_s = salary_data['uq_s']
            self.pop_s = salary_data['pop_s']
            self.resp_s = salary_data['resp_s']

            self.lq_ni = salary_data['lq_ni']
            self.med_ni = salary_data['med_ni']
            self.uq_ni = salary_data['uq_ni']
            self.pop_ni = salary_data['pop_ni']
            self.resp_ni = salary_data['resp_ni']

            self.lq_nw = salary_data['lq_nw']
            self.med_nw = salary_data['med_nw']
            self.uq_nw = salary_data['uq_nw']
            self.pop_nw = salary_data['pop_nw']
            self.resp_nw = salary_data['resp_nw']

            self.lq_ne = salary_data['lq_ne']
            self.med_ne = salary_data['med_ne']
            self.uq_ne = salary_data['uq_ne']
            self.pop_ne = salary_data['pop_ne']
            self.resp_ne = salary_data['resp_ne']

            self.lq_em = salary_data['lq_em']
            self.med_em = salary_data['med_em']
            self.uq_em = salary_data['uq_em']
            self.pop_em = salary_data['pop_em']
            self.resp_em = salary_data['resp_em']

            self.lq_wm = salary_data['lq_wm']
            self.med_wm = salary_data['med_wm']
            self.uq_wm = salary_data['uq_wm']
            self.pop_wm = salary_data['pop_wm']
            self.resp_wm = salary_data['resp_wm']

            self.lq_ee = salary_data['lq_ee']
            self.med_ee = salary_data['med_ee']
            self.uq_ee = salary_data['uq_ee']
            self.pop_ee = salary_data['pop_ee']
            self.resp_ee = salary_data['resp_ee']

            self.lq_se = salary_data['lq_se']
            self.med_se = salary_data['med_se']
            self.uq_se = salary_data['uq_se']
            self.pop_se = salary_data['pop_se']
            self.resp_se = salary_data['resp_se']

            self.lq_sw = salary_data['lq_sw']
            self.med_sw = salary_data['med_sw']
            self.uq_sw = salary_data['uq_sw']
            self.pop_sw = salary_data['pop_sw']
            self.resp_sw = salary_data['resp_sw']

            self.lq_yh = salary_data['lq_yh']
            self.med_yh = salary_data['med_yh']
            self.uq_yh = salary_data['uq_yh']
            self.pop_yh = salary_data['pop_yh']
            self.resp_yh = salary_data['resp_yh']

            self.lq_lo = salary_data['lq_lo']
            self.med_lo = salary_data['med_lo']
            self.uq_lo = salary_data['uq_lo']
            self.pop_lo = salary_data['pop_lo']
            self.resp_lo = salary_data['resp_lo']

            self.lq_ed = salary_data['lq_ed']
            self.med_ed = salary_data['med_ed']
            self.uq_ed = salary_data['uq_ed']
            self.pop_ed = salary_data['pop_ed']
            self.resp_ed = salary_data['resp_ed']

            self.lq_gl = salary_data['lq_gl']
            self.med_gl = salary_data['med_gl']
            self.uq_gl = salary_data['uq_gl']
            self.pop_gl = salary_data['pop_gl']
            self.resp_gl = salary_data['resp_gl']

            self.lq_cf = salary_data['lq_cf']
            self.med_cf = salary_data['med_cf']
            self.uq_cf = salary_data['uq_cf']
            self.pop_cf = salary_data['pop_cf']
            self.resp_cf = salary_data['resp_cf']

            self.unavail_reason = salary_data['unavail_reason']
            self.aggregate = salary_data['agg']

            self.unavailable_reason_region_not_exists = ""
            self.unavailable_reason_region_not_nation = ""
            self.unavailable_reason_region_is_ni = ""

            self.unavail_text_region_not_exists_english = salary_data['unavail_text_region_not_exists_english']
            self.unavail_text_region_not_exists_welsh = salary_data['unavail_text_region_not_exists_welsh']

            if 'unavail_text_region_not_nation_english' in salary_data:
                self.unavail_text_region_not_nation_english = salary_data['unavail_text_region_not_nation_english']
                self.unavail_text_region_not_nation_welsh = salary_data['unavail_text_region_not_nation_welsh']

            if 'unavail_text_region_is_ni_english' in salary_data:
                self.unavail_text_region_is_ni_english = salary_data['unavail_text_region_is_ni_english']
                self.unavail_text_region_is_ni_welsh = salary_data['unavail_text_region_is_ni_welsh']

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason_region_not_exists:
            unavailable["unavailable_region_not_exists"] = self.unavailable_reason_region_not_exists
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["unavailable_region_not_exists"] = self.unavail_text_region_not_exists_english if self.unavail_text_region_not_exists_english \
                    else self.unavail_text_region_not_exists_welsh
            else:
                unavailable["unavailable_region_not_exists"] = self.unavail_text_region_not_exists_welsh if self.unavail_text_region_not_exists_welsh else self.unavail_text_region_not_exists_english

        if self.unavailable_reason_region_not_nation:
            unavailable["unavailable_region_not_nation"] = self.unavailable_reason_region_not_nation
        elif hasattr(self, 'unavail_text_region_not_nation_english'):
            if self.display_language == enums.languages.ENGLISH:
                unavailable["unavailable_region_not_nation"] = self.unavail_text_region_not_nation_english if self.unavail_text_region_not_nation_english \
                    else self.unavail_text_region_not_nation_welsh
            else:
                unavailable["unavailable_region_not_nation"] = self.unavail_text_region_not_nation_welsh if self.unavail_text_region_not_nation_welsh else self.unavail_text_region_not_nation_english

        if self.unavailable_reason_region_is_ni:
            unavailable["unavailable_region_is_ni"] = self.unavailable_reason_region_is_ni
        elif hasattr(self, 'unavail_text_region_is_ni_english'):
            if self.display_language == enums.languages.ENGLISH:
                unavailable["unavailable_region_is_ni"] = self.unavail_text_region_is_ni_english if self.unavail_text_region_is_ni_english \
                    else self.unavail_text_region_is_ni_welsh
            else:
                unavailable["unavailable_region_is_ni"] = self.unavail_text_region_is_ni_welsh if self.unavail_text_region_is_ni_welsh else self.unavail_text_region_is_ni_english

        # if self.display_language == enums.languages.ENGLISH:
        #     unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
        #         else self.unavailable_url_welsh
        # else:
        #     unavailable["url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english
        
        unavailable["unavailable_region_not_exists_heading"], unavailable["unavailable_region_not_exists_body"] = separate_unavail_reason(unavailable["unavailable_region_not_exists"])

        return unavailable


def separate_unavail_reason(reason_unseparated):
    index_of_delimiter = reason_unseparated.find('\n\n')

    if index_of_delimiter > 4:
        reason_heading = reason_unseparated[:index_of_delimiter]
        reason_body = reason_unseparated[index_of_delimiter+2:]
    else:
        reason_heading = reason_unseparated
        reason_body = ""

    return reason_heading, reason_body
