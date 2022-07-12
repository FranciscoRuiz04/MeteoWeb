import requests
from bs4 import BeautifulSoup
import pandas as pd

# class Crawler:

#     def __init__(self, urls=[]):
#         self.visited_urls = []
#         self.urls_to_visit = urls

#     def download_url(self, url):
#         return requests.get(url)

#     def get_linked_urls(self, html):
#         soup = BeautifulSoup(html.content, 'html.parser')
#         for link in soup.find_all('tab'):
#             path = link.get('href')
#             if path and path.startswith('/'):
#                 path = 'https://www.meteoblue.com' + path
#             yield path

#     # def add_url_to_visit(self, url):
#     #     if url not in self.visited_urls and url not in self.urls_to_visit:
#     #         self.urls_to_visit.append(url)

#     def crawl(self, url):
#         html = self.download_url(url)
#         l = []
#         for url in self.get_linked_urls(html):
#             l.append(url)
#         return l
#         #     return url
#             # self.add_url_to_visit(url)

#     def run(self):
#         while self.urls_to_visit:
#             url = self.urls_to_visit.pop(0)
#             try:
#                 self.crawl(url)
#             except Exception:
#                 print(f'Failed to crawl: {url}')
#             finally:
#                 return self.crawl(url)
#             #     self.visited_urls.append(url)

# if __name__ == '__main__':
#     c = Crawler(urls=['https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270'])
#     print(c.run())


# url = r"https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270"
# req = requests.get(url)

# soup = BeautifulSoup(req.content, 'html.parser')
# results = soup.find_all('div', class_='tab')

# for result in results:
#     print(result)
    # childRes = result.find_all('div', class_='tab-temp-max')
    # print(childRes)




def genLinks(item):
    for i in item:
        links = i.find('a')
        path = links.get('href')
        if path and path.startswith('/'):
            path = 'https://www.meteoblue.com' + path
        yield path

def get_linked_urls(html, item, att = False):
    soup = BeautifulSoup(html.content, 'html.parser')
    labels = (label for label in soup.find_all(class_=item))
    if att:
        links = genLinks(labels)
        for link in links:
            yield link
    else:
        return next(labels)



# class DairyForecast:
#     def __init__(self, url):
#         self.url = url
    
#     def wrap(fun):
#         def req_html(self, *args, **kargs):
#             req = requests.get(self.url)
#             soup = BeautifulSoup(req.content, 'html.parser')
#             decoratedFun = fun(*args, **kargs)
#         return req_html


url = r"https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270"
req = requests.get(url)
g = get_linked_urls(req, 'tab', True)
next(g)
for x in g:
    print(x)