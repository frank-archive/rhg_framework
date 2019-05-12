from wordpress_utils import get_wordpress_version
import argparse

p = argparse.ArgumentParser()
p.add_argument('--url', '-u', type=str)
args = p.parse_args()


print('vulnerable' if get_wordpress_version(
    args.url
) == "4.6" else '')
