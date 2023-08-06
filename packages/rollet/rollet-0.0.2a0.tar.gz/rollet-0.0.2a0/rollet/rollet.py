"""
Rollet functions
"""

__all__ = [
    "get_content"
]

from datetime import datetime
from tldextract import extract
from requests.exceptions import ConnectTimeout

from rollet import settings
from rollet.utils import lookup
from rollet.extractor import (
    BaseExtractor
)

def get_content(url):
    """
    Pull content from url to formated data
    url: string url
    :return: dict of content
    """
    content = {
        'url': url,
        'status': None,
        'title': 'blacklisted',
        'abstract': None,
        'lang': None,
        'content_type': None,
        'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    domain = extract(url).domain
    if domain in settings.BLACKLIST: return content
    f_kwargs = settings.FETCH_KWARGS[settings.TYPES.get(domain, 'default')]
    extractor = lookup(
        url,
        settings.EXTRACTORS.get(domain, settings.EXTRACTORS['default']))
    extractor = extractor if extractor else BaseExtractor
    try:
        content = extractor(url, **f_kwargs).to_dict()
    except ConnectTimeout:
        content['title'] = "Timeout error"
    except Exception as e:
        content['title'] = str(e)
    return content