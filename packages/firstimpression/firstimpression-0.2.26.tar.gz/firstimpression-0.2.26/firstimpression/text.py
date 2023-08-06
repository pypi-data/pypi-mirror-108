import datetime


def remove_tags_from_string(tags, text):
    return tags.sub('', text)


def replace_html_entities(replace_dict, text):
    for key in replace_dict:
        text = text.replace(key, replace_dict[key])
        text = text.strip()
    return text


def get_locale_month(month_number, month_index):
    return{
        1: ['jan', 'januari'],
        2: ['feb', 'februari'],
        3: ['maa', 'maart'],
        4: ['apr', 'april'],
        5: ['mei', 'mei'],
        6: ['jun', 'juni'],
        7: ['jul', 'juli'],
        8: ['aug', 'augustus'],
        9: ['sep', 'september'],
        10: ['okt', 'oktober'],
        11: ['nov', 'november'],
        12: ['dec', 'december']
    }[month_number][month_index]


def parse_datetime(datetime_object, month_index):
    day = str(datetime_object.day)
    month = get_locale_month(datetime_object.month, month_index)
    return ' '.join([day, month, datetime.datetime.strftime(datetime_object, '%Y %H:%M')])
