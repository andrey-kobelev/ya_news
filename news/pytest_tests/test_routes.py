from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .constants import (
    HOME,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
)

READER = pytest.lazy_fixture('reader_client')
AUTHOR = pytest.lazy_fixture('author_client')
ANONYM = pytest.lazy_fixture('client')

LOGIN_TO_EDIT_REDIRECT = pytest.lazy_fixture('next_from_login_to_edit_url')
LOGIN_TO_DELETE_REDIRECT = pytest.lazy_fixture('next_from_login_to_delete_url')

DETAIL = pytest.lazy_fixture('detail_url')
DELETE = pytest.lazy_fixture('delete_url')
EDIT = pytest.lazy_fixture('edit_url')

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client_, status',
    (
        (DETAIL, ANONYM, HTTPStatus.OK),
        (DETAIL, AUTHOR, HTTPStatus.OK),
        (HOME, ANONYM, HTTPStatus.OK),
        (LOGIN_URL, ANONYM, HTTPStatus.OK),
        (LOGOUT_URL, ANONYM, HTTPStatus.OK),
        (SIGNUP_URL, ANONYM, HTTPStatus.OK),
        (EDIT, AUTHOR, HTTPStatus.OK),
        (EDIT, READER, HTTPStatus.NOT_FOUND),
        (DELETE, AUTHOR, HTTPStatus.OK),
        (DELETE, READER, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_availability(
    url, client_, status
):
    assert client_.get(url).status_code == status


@pytest.mark.parametrize(
    'url, login_next_url, client_',
    (
        (EDIT, LOGIN_TO_EDIT_REDIRECT, ANONYM),
        (DELETE, LOGIN_TO_DELETE_REDIRECT, ANONYM)
    )
)
def test_redirect_for_anonym_client(url, login_next_url, client_):
    assertRedirects(client_.get(url), login_next_url)
