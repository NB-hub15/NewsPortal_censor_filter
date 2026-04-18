from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise TypeError('Фильтр censor применяется только к строкам')

    words = value.split()
    result = []

    for word in words:
        word = word[0] + '*' * (len(word) - 1)
        result.append(word)

    return ' '.join(result)