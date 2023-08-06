from facebook_scraper import *
import argparse
import logging


def enable_logging_to_file():
    logger = logging.getLogger('facebook_scraper')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

    file_handler = logging.FileHandler('logs/debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def write_post_to_disk(post):
    filename = f'{post["post_id"]}.json'
    with open(f'output/{filename}', mode='wt') as file:
        json.dump(post, file, indent=4, default=str)


def write_posts_to_disk(posts, filename):
    keys = posts[0].keys()
    with open(filename, 'w', encoding=locale.getpreferredencoding()) as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(posts)

def run():
    parser = argparse.ArgumentParser()

    parser.add_argument('group_id', type=str, help="Facebook group id")
    parser.add_argument('--proxy', type=str, help="Proxy server address", default=None)
    parser.add_argument('--pages', type=int, help="Number of pages to download", default=5)
    parser.add_argument('--debug', type=bool, help="Enable debug", default=False)
    parser.add_argument('--filename', type=str, help="Output file", default='posts.csv')

    args = parser.parse_args()
    print(args)

    if args.debug:
        enable_logging_to_file()

    count = 0
    list_of_posts = []
    options = {
        "page_limit": args.pages,
    }

    scraper = FacebookScraper()
    if args.proxy:
        scraper.requests_kwargs.update({
            'proxies': {
                'http': args.proxy,
                'https': args.proxy,
            }
        })


    for post in scraper.get_group_posts(args.group_id, **options):
        print(f'{count + 1} => {post["post_id"]}, {post["time"]}')

        if args.debug:
            write_post_to_disk(post)

        list_of_posts.append(post)

        count += 1

    if count == 0:
        logger.warning("No posts found. Is your IP banend?")
        exit(1)

    write_posts_to_disk(list_of_posts, args.filename)

if __name__ == '__main__':
    run()