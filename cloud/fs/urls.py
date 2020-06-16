from django.urls import path, include

from .views import dialplan

app_name = 'fs'

urlpatterns = [
    # config
    # cdr
    path('dialplan', dialplan.DialplanViews.as_view()),
]
