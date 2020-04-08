from django import template

register = template.Library()


@register.simple_tag()
def cut(s):
    return s[:256]


@register.simple_tag()
def mail(s):
    if s == "Username:":
        return "email"
    else:
        return s

# TODO: check on the cut
