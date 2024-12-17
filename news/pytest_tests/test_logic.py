from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from . import constants as consts

BAD_WORDS_DATA_FOR_COMMENT = {
    'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
}

COMMENT_FORM_DATA = {
    'text': consts.COMMENT_TEXT
}

NEW_COMMENT_FORM_DATA = {'text': f'{consts.NEW_COMMENT_TEXT} bla bla'}

pytestmark = pytest.mark.django_db


def test_anonym_cant_create_comment(
    client, news, detail_url, next_from_login_to_create_url
):
    comments = sorted(Comment.objects.all())
    response = client.post(detail_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, next_from_login_to_create_url)
    assert sorted(Comment.objects.all()) == comments


def test_user_can_create_comment(
    author_client, news, author, detail_url, url_to_comments
):
    Comment.objects.all().delete()
    author_client.post(detail_url, data=COMMENT_FORM_DATA)
    assert Comment.objects.count() == 1
    comment = Comment.objects.last()
    assert comment.text == COMMENT_FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news


def test_user_cant_use_bad_words(
    author_client, news, detail_url, author
):
    comments = sorted(
        Comment.objects.all()
    )
    response = author_client.post(
        detail_url, data=BAD_WORDS_DATA_FOR_COMMENT
    )
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert sorted(
        Comment.objects.all()
    ) == comments


def test_author_can_delete_comment(
    author_client, comment, delete_url,
    url_to_comments, news, author
):
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_not_author_cant_delete_comment_of_author(
    reader_client, comment, delete_url, author, news
):
    comments = sorted(
        Comment.objects.all()
    )
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comments == sorted(
        Comment.objects.all()
    )
    comment_db = Comment.objects.get(pk=comment.pk)
    assert comment_db.text == comment.text
    assert comment_db.author == comment.author
    assert comment_db.news == comment.news


def test_author_can_edit_comment(
    author_client, comment, news, url_to_comments, edit_url, author
):
    response = author_client.post(edit_url, data=NEW_COMMENT_FORM_DATA)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.filter(pk=comment.pk).exists()
    comment_db = Comment.objects.get(pk=comment.pk)
    assert comment_db.text == NEW_COMMENT_FORM_DATA['text']
    assert comment_db.author == comment.author
    assert comment_db.news == comment.news


def test_not_author_cant_edit_comment_of_author(
    reader_client, comment, news, author, edit_url
):
    comments_count = Comment.objects.count()
    response = reader_client.post(edit_url, data=NEW_COMMENT_FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count
    assert Comment.objects.filter(pk=comment.pk).exists()
    comment_db = Comment.objects.get(pk=comment.pk)
    assert comment_db.text == comment.text
    assert comment_db.author == comment.author
    assert comment_db.news == comment.news
