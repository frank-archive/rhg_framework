from wordpress_utils import get_wordpress_version
import json

url = json.loads(input())['url']

print('vulnerable' if get_wordpress_version(url) == "4.6" else '')
