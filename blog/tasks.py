import os
import shutil
import time
import wget
from urllib.error import URLError
from django.utils import timezone
from import_export.formats import base_formats
from .site_settings import MAX_RETRIES, RETRY_DELAY
from .models import Article, Author, KeyWord, KeyWordResult, KeyWordResultItem, ArticleTag, Category, Tag
from .resources import ArticleResource
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from celery import shared_task
from celery import chain


options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')


@shared_task
def article_scrapper_search(url, keyword, path, export_format):
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(url)
    except WebDriverException as error:
        print(f'Web Driver Exception {error}')

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    category = ''
    category_link = ''
    try:
        element = driver.find_element(By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]')
        element.click()
    except NoSuchElementException:
        print('there was no cookies')
    try:
        header = soup.find('header', class_='article__header')
        title = header.find('h1').text
        if header.find('div', class_='article__primary-category'):
            category = header.find('div', class_='article__primary-category').find('a').text
            category_link = f"{url}{header.find('div', class_='article__primary-category').find('a').get('href')}"
        elif header.find('h3', class_='article__event-title'):
            category = 'event'
            category_link = f"{url}{header.find('h3', class_='article__event-title').find('a').get('href')}"
        elif header.find('div', class_='featured-article__label'):
            category = 'Featured Article'

        posted = timezone.make_aware(timezone.datetime.fromisoformat(header.find('time').get('datetime')))
        author = header.find('div', class_='article__byline-wrapper').find('a').text
        author_link = f"{url}{header.find('div', class_='article__byline-wrapper').find('a').get('href')}"
        content = soup.find_all('div', class_='article__content-wrap')[1]
        image_link = content.find('img').get('src')
        text = ', '.join(i.text for i in content.find('div', class_='article-content').find_all('p'))
        tags = list(Tag.objects.get_or_create(title=i.text, link=i.find('a').get('href'))[0]
                    for i in soup.find('div', class_='article__related-links').find_all('li'))

        category_instance, _ = Category.objects.get_or_create(
            title=category,
            link=category_link,
        )
        author_instance, _ = Author.objects.get_or_create(
            title=author,
            link=author_link,
        )
        article_instance, _ = Article.objects.get_or_create(
            title=title,
            link=url,
            description=text,
            posted=posted,
            author=author_instance,
            category=category_instance,
            is_download=True,
        )
        for tag in tags:
            ArticleTag.objects.get_or_create(
                article=article_instance,
                tag=tag,
            )
        keyword_instance, _ = KeyWord.objects.get_or_create(
            title=keyword,
        )
        keyword_result_instance, _ = KeyWordResult.objects.get_or_create(
            keyword=keyword_instance,
        )
        KeyWordResultItem.objects.create(
            keyword_result=keyword_result_instance,
            article=article_instance
        )
        zip_creator(image_link, path, export_format)

    except AttributeError as error:
        print(f'Attribute Error {error}')
    finally:
        driver.quit()


@shared_task
def search_scrapper(phrase, path, export_format):
    url = f'https://search.techcrunch.com/search;?p={phrase}'
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(url)
    except WebDriverException as error:
        print(f'Web Driver Exception {error}')
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        ul = soup.find('ul', class_='compArticleList')
        for li in ul.find_all('li'):
            title = li.find('h4').find('a').text
            link = li.find('a').get('href')
            if not Article.objects.filter(title=title).exists():
                article_scrapper_search.delay(link, phrase, path, export_format)

    except AttributeError as error:
        print(f'Attribute Error {error}')
    finally:
        driver.quit()


@shared_task
def article_scrapper(url):
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(url)
    except WebDriverException as error:
        print(f'Web Driver Exception {error}')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    category = ''
    category_link = ''
    try:
        element = driver.find_element(By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]')
        element.click()
    except NoSuchElementException:
        print('there was no cookies')

    try:
        header = soup.find('header', class_='article__header')
        title = header.find('h1').text
        if header.find('div', class_='article__primary-category'):
            category = header.find('div', class_='article__primary-category').find('a').text
            category_link = f"{url}{header.find('div', class_='article__primary-category').find('a').get('href')}"
        elif header.find('h3', class_='article__event-title'):
            category = 'event'
            category_link = f"{url}{header.find('h3', class_='article__event-title').find('a').get('href')}"
        elif header.find('div', class_='featured-article__label'):
            category = 'Featured Article'

        posted = timezone.make_aware(timezone.datetime.fromisoformat(header.find('time').get('datetime')))
        author = header.find('div', class_='article__byline-wrapper').find('a').text
        author_link = f"{url}{header.find('div', class_='article__byline-wrapper').find('a').get('href')}"
        content = soup.find_all('div', class_='article__content-wrap')[1]
        image_link = content.find('img').get('src')
        # downloader.delay(image_link)
        text = ', '.join(i.text for i in content.find('div', class_='article-content').find_all('p'))
        tags = list(Tag.objects.get_or_create(title=i.text, link=i.find('a').get('href'))[0]
                    for i in soup.find('div', class_='article__related-links').find_all('li'))

        category_instance, _ = Category.objects.get_or_create(
            title=category,
            link=category_link,
        )
        author_instance, _ = Author.objects.get_or_create(
            title=author,
            link=author_link,
        )
        article_instance, _ = Article.objects.get_or_create(
            title=title,
            link=url,
            description=text,
            posted=posted,
            author=author_instance,
            category=category_instance,
        )
        for tag in tags:
            ArticleTag.objects.get_or_create(
                article=article_instance,
                tag=tag,
            )
    except AttributeError as error:
        print(f'Attribute Error {error}')
    finally:
        driver.quit()


@shared_task
def main_page():
    driver = webdriver.Firefox(options=options)
    url = f'https://techcrunch.com'
    try:
        driver.get(url)
    except WebDriverException as error:
        print(f'Web Driver Exception {error}')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        element = driver.find_element(By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]')
        element.click()
    except NoSuchElementException:
        print('there was no cookies')
    try:
        island = soup.find('div', class_="feature-island").find_all('div')
        for i, j in enumerate(island):
            if i == 0:
                link = f"{url}{j.find('h2', class_='fi-main-block__title').find('a').get('href')}"
                if Article.objects.filter(link=link).exists():
                    article_scrapper.delay(link)
            if i == 1:
                for m in j.find_all('article'):
                    link = f"{url}{m.find('h3').find('a').get('href')}"
                    if Article.objects.filter(link=link).exists():
                        article_scrapper.delay(link)

        main_content = soup.find('div', class_='river')
        for i in main_content.find('div').find_all('article'):
            header = i.find('header')
            link = f"{url}{header.find('h2').find('a').get('href')}"
            if Article.objects.filter(link=link).exists():
                article_scrapper.delay(link)

    except AttributeError as error:
        print(f'Attribute Error {error}')
    finally:
        driver.quit()


@shared_task
def category_scrapper(base, kind):
    driver = webdriver.Firefox(options=options)
    url = f'https://techcrunch.com/{base}/{kind}'
    try:
        driver.get(url)
    except WebDriverException as error:
        print(f'Web Driver Exception {error}')
    try:
        element = driver.find_element(By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]')
        element.click()
    except NoSuchElementException:
        print('there was no cookies')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        soup = soup.find('div', class_='river')
        for post in soup.find_all('article'):
            link = f"{url}{post.find('h2').find('a').get('href')}"

            if Article.objects.filter(link=link).exists():
                article_scrapper.delay(link)
    except AttributeError as error:
        print(f'Attribute Error {error}')
    finally:
        driver.quit()


@shared_task
def daily_scrapper():
    web_pages = ['startups', 'venture', 'security', 'artificial-intelligence', 'cryptocurrency',
                 'apps', 'fintech', 'hardware', 'transportation', 'media-entertainment'
                 ]
    tech_plus_category = ['fundraising', 'events', 'growth',
                          'investor-surveys', 'market-analysis', 'work'
                          ]
    main_page.delay()
    for i in web_pages:
        category_scrapper.delay('category', i)
    for i in tech_plus_category:
        category_scrapper.delay('techcrunchplus', i)


@shared_task
def downloader(url, file_path):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            wget.download(
                url,
                file_path,
                bar=wget.bar_adaptive
            )
            break
        except URLError as error:
            print(f'URL Error {error}')
            if attempt < MAX_RETRIES:
                print(f'Retrying in {RETRY_DELAY}')
                time.sleep(RETRY_DELAY)
            else:
                print(f"couldn't download {url}")


def zip_creator(link, path, export_format):
    task_chain = chain(downloader.s(link, path))
    result = task_chain.apply_async()
    result.get()

    if Article.objects.filter(is_download=True).exists():
        print('inside the function')
        article_resource = ArticleResource()
        dataset = article_resource.export()

        if export_format == 'csv':
            export_path = os.path.join(path, 'exported_data.csv')
            exported_data = base_formats.CSV().export_data(dataset)
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(exported_data)
        elif export_format == 'xls':
            export_path = os.path.join(path, 'exported_data.xls')
            exported_data = base_formats.XLS().export_data(dataset)
            with open(export_path, 'wb') as f:
                f.write(exported_data)
        elif export_format == 'json':
            export_path = os.path.join(path, 'exported_data.json')
            exported_data = base_formats.JSON().export_data(dataset)
            with open(export_path, 'w') as f:
                f.write(exported_data)
        shutil.make_archive(f'{path}_', 'zip', path)
        Article.objects.update(is_download=False)
