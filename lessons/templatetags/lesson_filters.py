from django import template

register = template.Library()

@register.filter
def has_submitted(lesson, user):
    return lesson.submissions.filter(student=user).exists()