import pytest
from django.conf import settings

from news.forms import CommentForm
from . import constants as consts

pytestmark = pytest.mark.django_db


def test_comments_order(news, client, comments_bulk_create, detail_url):
    context = client.get(detail_url).context
    assert 'news' in context, 'Новости нет в контексте'
    comments_created_dates = [
        comment.created
        for comment in context['news'].comment_set.all()
    ]
    assert comments_created_dates == sorted(comments_created_dates)


def test_anonym_has_no_form(client, news, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_auth_client_has_form(author_client, news, detail_url):
    context = author_client.get(detail_url).context
    assert 'form' in context
    assert isinstance(context['form'], CommentForm)


def test_news_count(news_bulk_create, client):
    context = client.get(consts.HOME).context
    assert len(context['object_list']) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(news_bulk_create, client):
    all_news = client.get(consts.HOME).context['object_list']
    all_news_dates = [news.date for news in all_news]
    assert all_news_dates == sorted(all_news_dates, reverse=True)
