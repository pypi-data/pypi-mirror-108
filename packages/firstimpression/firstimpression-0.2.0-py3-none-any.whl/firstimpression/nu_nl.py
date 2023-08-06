import datetime
import time
import os
from .scala import *


def get_datetime_object(item):
    unparsedpubdate = item.find('pubDate').text
    # Wed, 23 Oct 2019 15:03:33 +0200

    created_at = datetime.datetime.strptime(
        unparsedpubdate, "%a, %d %b %Y %H:%M:%S {}".format(unparsedpubdate[-5:])).timetuple()
    return datetime.datetime.fromtimestamp(time.mktime(created_at))


def get_medialink(item):
    return item.find('enclosure').attrib['url']


def install_picture_content_wrap(picture_format, subdirectory, news_item):
    # Installs content to LocalIntegratedContent folder and returns mediapath
    if not picture_format in picture_formats:
        return None

    media_link = get_medialink(news_item).replace("_sqr256", "")

    if picture_format == 'square':
        media_link = media_link.replace('.jpg', '_sqr512.jpg')

    media_path = download_media(
        PICTURE_FORMATS_DICT[picture_format] + media_link, subdirectory)

    # if not check_valid_jpeg(media_path):
    #     return False
    scala.install_content(media_path, subdirectory, True)

    media_filename = media_path.split('\\').pop()

    return os.path.join('Content:\\', subdirectory, media_filename)
