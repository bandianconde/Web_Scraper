import requests
import string
import os
from bs4 import BeautifulSoup


def clean_article_title(title):
    title = title.strip(' ')
    for punct in string.punctuation:
        title = title.replace(punct, '_')
    title = title.replace(' ', '_')
    return title


def get_article_body(article_url):
    response = requests.get(article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(response.content, 'html.parser')
    article_body = soup.find('div', {'class': "c-article-body main-content"})
    article_body_text = article_body.get_text().strip()
    return article_body_text


def get_articles(response, article_type, page_directory):
    prefix = "https://nature.com"
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('li', {"class": "app-article-list-row__item"})
    for article in articles:
        title_tag = article.find('a', {'data-track-action': "view article"})
        title = clean_article_title(title_tag.get_text())
        span_for_article_type = article.find('span', {"data-test": "article.type"}).find('span').string.strip()
        if span_for_article_type == article_type:
            article_url = f"{prefix}{title_tag.get('href')}"
            article_body_text = get_article_body(article_url)
            with open(f'{page_directory}/{title}.txt', 'w') as article_file:
                article_file.write(article_body_text)
    next_path = soup.find('li', {'data-test': 'page-next'}).find('a').get('href')
    next_path = f'{prefix}{next_path}'
    return next_path


number_of_pages = int(input())
article_type = input()
url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
for n in range(number_of_pages):
    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    page_directory = f'Page_{n + 1}'
    os.mkdir(page_directory)
    url = get_articles(response, article_type, page_directory)
