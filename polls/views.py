from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Poll, Option, Vote
from .serializers import PollCreateSerializer, PollDetailSerializer, VoteSerializer, OptionSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.core.cache import cache


@extend_schema(
    request=PollCreateSerializer,
    responses={201: PollDetailSerializer},
    examples=[
        OpenApiExample(
            'Create poll example',
            summary='Create a poll with 3 options',
            value={
                'title': 'Favorite language',
                'description': 'Pick one',
                'options': ['Python', 'JavaScript', 'Go']
            },
            request_only=True,
        )
    ],
)
class PollCreateView(generics.CreateAPIView):
    serializer_class = PollCreateSerializer
    queryset = Poll.objects.all()


@extend_schema(responses=PollDetailSerializer)
class PollDetailView(generics.RetrieveAPIView):
    serializer_class = PollDetailSerializer
    queryset = Poll.objects.prefetch_related('options')


@extend_schema(
    request=VoteSerializer,
    responses={201: VoteSerializer, 400: None},
    examples=[
        OpenApiExample(
            'Vote example',
            summary='Cast a vote for an option',
            value={'poll': '00000000-0000-0000-0000-000000000000', 'option': '00000000-0000-0000-0000-000000000001', 'voter_id': 'user-123'},
            request_only=True,
        )
    ],
)
class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


@extend_schema(responses={200: OpenApiExample('Results', value={'total_votes': 10, 'results': [{'id': 'uuid','text':'A','votes':7}]})})
class PollResultsView(APIView):
    def get(self, request, pk):
        cache_key = f"poll_results:{pk}"
        # try cached value first
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        poll = get_object_or_404(Poll.objects.prefetch_related('options'), pk=pk)
        # annotate options with vote counts efficiently
        options = Option.objects.filter(poll=poll).annotate(votes=Count('votes')).order_by('order')
        serializer = OptionSerializer(options, many=True)
        data = {
            'poll_id': str(poll.id),
            'title': poll.title,
            'results': serializer.data,
            'total_votes': sum(item['votes'] for item in serializer.data)
        }
        # cache results for short period; invalidated by signals when votes/options change
        cache.set(cache_key, data, timeout=30)  # 30 seconds default; tune as needed
        return Response(data)
