from django import template

from courses.models import Course


register = template.Library()

@register.inclusion_tag('students/course/list.html')
def student_list_courses(user):
    courses = Course.objects.filter(students__in=[user])
    return {'object_list': courses}