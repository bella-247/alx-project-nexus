from django.urls import path
from .views import PollCreateView, PollDetailView, VoteCreateView, PollResultsView

urlpatterns = [
    path('polls/', PollCreateView.as_view(), name='poll-create'),
    path('polls/<uuid:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/<uuid:pk>/results/', PollResultsView.as_view(), name='poll-results'),
    path('votes/', VoteCreateView.as_view(), name='vote-create'),
]
