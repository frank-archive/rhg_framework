from wordpress_utils import get_wordpress_version
import json

url = 'http://'+json.loads(input())['attack']['server_ip']

print('vulnerable' if get_wordpress_version(url) == "4.6" else '')
