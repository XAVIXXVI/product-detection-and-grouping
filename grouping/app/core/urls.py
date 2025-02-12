from django.urls import path
from .views import GroupingView

urlpatterns = [
    path('grouping/', GroupingView.as_view(), name='grouping'),

]
