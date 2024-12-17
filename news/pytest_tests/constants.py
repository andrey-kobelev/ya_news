from django.urls import reverse

LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Новый текст комментария'
NUM_COMMENTS_FOR_ORDER = 5

NEXT = '{}?next={}'

HOME = reverse('news:home')
