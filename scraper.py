import requests
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import json
import os
import re

@dataclass
class MJScrapeper:
    base_url: str

    def fetch(self, url):
        with requests.Session() as session:
            response = session.get(url)
        return response.text

    def parse(self, html):
        tree = HTMLParser(html)
        json_data = json.loads(tree.css_first('script#__NEXT_DATA__').text())
        json_formatted_str = json.dumps(json_data, indent=2)
        print(json_formatted_str)
        i = 0
        items = []
        item = {'id': None, 'filename': None, 'url': None}
        while 1:
            try:
                item['id'] = json_data['props']['pageProps']['jobs'][i]['id']
                item['url'] = json_data['props']['pageProps']['jobs'][i]['event']['seedImageURL']
                item['filename'] = '_'.join(re.findall(r"[a-zA-Z0-9,]+",json_data['props']['pageProps']['jobs'][i]['prompt']))
                i += 1
                if url != None:
                    items.append(item.copy())
            except Exception as e:
                print(e)
                break
        return items

    def download_img(self, items):
        if not os.path.exists('img_result'):
            os.mkdir('img_result')
        for i, item in enumerate(items):
            print(item)
            if item != None:
                with requests.Session() as session:
                    response = session.get(item['url'])
                with open(f"img_result/{str(i+1)} {item['filename'].split(',')[0]}_{item['id']}.png", 'wb') as f:
                    f.write(response.content)
            else:
                continue
            print('Image downloaded successfully!')

if __name__ == '__main__':
    base_url = 'https://www.midjourney.com'
    scraper = MJScrapeper(base_url=base_url)
    url = 'https://www.midjourney.com/showcase/recent/'
    html = scraper.fetch(url)
    img_urls = scraper.parse(html)
    scraper.download_img(img_urls)