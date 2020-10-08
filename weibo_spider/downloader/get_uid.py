import re

def get_uid(url):
    """get uid from url."""
    uid = re.findall('[0-9]+', url)[0]
    return uid
