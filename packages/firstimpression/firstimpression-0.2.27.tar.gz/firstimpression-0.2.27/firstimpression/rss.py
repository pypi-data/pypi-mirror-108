import requests
import xml.etree.ElementTree as ET


def get_feed(url):
    response = requests.get(url)
    return ET.fromstring(response.content)


def get_items_from_feed(feed, name):
    return feed.findall(name)
