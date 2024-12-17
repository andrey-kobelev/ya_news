from datetime import timedelta

import pytest
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.test import Client

from news.models import Comment, News
from . import constants as consts


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(django_user_model):
    reader = django_user_model.objects.create(username='Reader')
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости.'
    )


@pytest.fixture
def news_bulk_create():
    News.objects.bulk_create(
        News(title=f'Новость {index}', text='Просто текст.')
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 5)
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text=consts.COMMENT_TEXT,

    )


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse(
        'news:delete', args=(comment.id,)
    )


@pytest.fixture
def detail_url(news):
    return reverse(
        'news:detail', args=(news.id,)
    )


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'


@pytest.fixture
def comments_bulk_create(author, news):
    now = timezone.now()
    for index in range(consts.NUM_COMMENTS_FOR_ORDER):
        comment = Comment.objects.create(
            news=news, author=author, text=f'{consts.COMMENT_TEXT} {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def next_from_login_to_edit_url(edit_url):
    return consts.NEXT.format(consts.LOGIN_URL, edit_url)


@pytest.fixture
def next_from_login_to_delete_url(delete_url):
    return consts.NEXT.format(consts.LOGIN_URL, delete_url)


@pytest.fixture
def next_from_login_to_create_url(detail_url):
    return consts.NEXT.format(consts.LOGIN_URL, detail_url)
