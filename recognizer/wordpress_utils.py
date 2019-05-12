import requests
import re

VER_MATCH = r'wp-emoji-release\.min\.js\?ver=(.*)'

def get_wordpress_version(url):
    page = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
            'Connection': 'Close'
        }
    )
    result = re.findall(VER_MATCH, page.text)
    if len(result) != 0:
        return result[0]
    return -1