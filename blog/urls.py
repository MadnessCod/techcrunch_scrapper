from django.urls import path
from .views import search, main_page_scraper


urlpatterns = [
    path('search/', search, name='search'),
    path('daily_scrape/', main_page_scraper, name='daily scraper'),
]
