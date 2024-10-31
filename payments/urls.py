from django.urls import path
from .views import stk_push_view, callback_view

urlpatterns = [
    path('stk-push/', stk_push_view, name='stk_push'),
    path('callback/', callback_view, name='callback')
]
