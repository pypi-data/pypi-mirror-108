from .text import *


def get_title(item):
    title = item.find('title').text
    return title


def get_description(item):
    description = item.find('description').text
    return description
