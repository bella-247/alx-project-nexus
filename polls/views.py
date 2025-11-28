from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Poll, Option, Vote
from .serializers import PollCreateSerializer, PollDetailSerializer, VoteSerializer, OptionSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@extend_schema(
    request=PollCreateSerializer,
    responses={201: PollDetailSerializer},
    examples=[
        OpenApiExample(
            'Create poll example',
            summary='Create a poll with 3 options',
            value={
                'question': 'Favorite language',
                'description': 'Pick one',
                'options': ['Python', 'JavaScript', 'Go']
            },
            request_only=True,
        )
    ],
)
class PollListCreateView(generics.ListCreateAPIView):
    """GET: return {"polls": [...]}. POST: create a poll."""
    serializer_class = PollCreateSerializer
    queryset = Poll.objects.all().prefetch_related('options')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PollDetailSerializer
        return PollCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response({'polls': serializer.data})

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({'polls': serializer.data})

    def perform_create(self, serializer):
        # Pass request in serializer context so it can set created_by
        serializer.save()


@extend_schema(responses=PollDetailSerializer)
class PollDetailView(generics.RetrieveAPIView):
    serializer_class = PollDetailSerializer
    queryset = Poll.objects.prefetch_related('options')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        # support passing voter_id via query param `voter_id` to compute hasVoted and option.voted
        voter_id = self.request.query_params.get('voter_id') or self.request.query_params.get('userId')
        if voter_id:
            ctx['voter_id'] = voter_id
        ctx['request'] = self.request
        return ctx


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

    def create(self, request, *args, **kwargs):
        # If user is authenticated, do not rely on client-supplied userId
        data = request.data.copy()
        if request.user and request.user.is_authenticated:
            data['userId'] = str(request.user.id)
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        # allow marking voted option by passing voter_id or userId
        voter_id = request.query_params.get('voter_id') or request.query_params.get('userId')
        serializer = OptionSerializer(options, many=True, context={'voter_id': voter_id, 'request': request})
        data = {
            'id': str(poll.id),
            'question': poll.title,
            'description': poll.description,
            'options': serializer.data,
            'totalVotes': sum(item['votes'] for item in serializer.data),
            'createdAt': poll.created_at,
            'updatedAt': poll.updated_at,
            'isActive': poll.is_active,
            'views': poll.views,
            'hasVoted': bool((voter_id and Vote.objects.filter(poll=poll, voter_id=voter_id).exists()) or (not voter_id and request.user.is_authenticated and Vote.objects.filter(poll=poll, voter_id=str(request.user.id)).exists())),
            'createdBy': str(poll.created_by.id) if poll.created_by else None,
        }
        # cache results for short period; invalidated by signals when votes/options change
        cache.set(cache_key, data, timeout=30)  # 30 seconds default; tune as needed
        return Response(data)
