from .text import *


def get_title(item):
    title = item.find('title').text
    return replace_html_entities(REPLACE_DICT, title)


def get_description(item):
    description = item.find('description').text
    return remove_tags_from_string(TAGS_TO_REMOVE, description)
