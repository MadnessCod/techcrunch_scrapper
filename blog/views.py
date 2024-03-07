import os
import shutil

import celery
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, HttpResponse
from import_export.formats import base_formats
from .models import Article
from .resources import ArticleResource
from .forms import UserInputForm
from .tasks import daily_scrapper, search_scrapper
from celery import chain


# Create your views here.


def search(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            phrase = form.cleaned_data['phrase']
            export_format = form.cleaned_data['export_format']
            main_path = os.path.join(
                settings.MEDIA_ROOT,
                f'exported_data_{phrase}_{timezone.now().strftime("%Y-%m-%d_%H%M%S")}'
            )
            if not os.path.exists(main_path):
                os.makedirs(main_path, exist_ok=True)

            search_scrapper.delay(phrase, main_path, export_format)

            return HttpResponse(f'data will be available at {main_path}_.zip')

        else:
            form = UserInputForm()
            return render(request, 'enter_phrase.html', {'form': form})
    else:
        form = UserInputForm()
        return render(request, 'enter_phrase.html', {'form': form})


def main_page_scraper(request):
    daily_scrapper.delay()
    return HttpResponse('tasks started')


def checker():
    while len(celery.current_app.tasks.values()) != 0:
        print('success')
        break


checker()
