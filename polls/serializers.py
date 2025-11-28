from rest_framework import serializers
from .models import Poll, Option, Vote
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class OptionSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(read_only=True)
    voted = serializers.SerializerMethodField()

    class Meta:
        model = Option
        # frontend expects id, text, votes, voted
        fields = ('id', 'text', 'votes', 'voted')

    def get_voted(self, obj):
        # expects voter_id in serializer context to mark which option the voter chose
        # context may contain request or explicit voter_id
        voter_id = self.context.get('voter_id')
        if not voter_id and self.context.get('request') and getattr(self.context['request'], 'user', None) and self.context['request'].user.is_authenticated:
            voter_id = str(self.context['request'].user.id)
        if not voter_id:
            return False
        return Vote.objects.filter(poll=obj.poll, voter_id=voter_id, option=obj).exists()


class PollCreateSerializer(serializers.ModelSerializer):
    # frontend sends `question` instead of `title`
    question = serializers.CharField(source='title')
    options = serializers.ListField(child=serializers.CharField(max_length=255), write_only=True)
    createdBy = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Poll
        fields = ('id', 'question', 'description', 'expires_at', 'options', 'createdBy')

    def validate_expires_at(self, value):
        if value is not None and value <= timezone.now():
            raise serializers.ValidationError('expires_at must be in the future')
        return value

    def create(self, validated_data):
        options = validated_data.pop('options', [])
        # handle createdBy if provided (accept user id)
        created_by_val = validated_data.pop('createdBy', None)
        if created_by_val:
            try:
                user = User.objects.filter(id=created_by_val).first()
                if user:
                    validated_data['created_by'] = user
            except Exception:
                pass

        # if request user available and created_by not set, use it
        request = self.context.get('request')
        if not validated_data.get('created_by') and request and getattr(request, 'user', None) and request.user.is_authenticated:
            validated_data['created_by'] = request.user

        poll = Poll.objects.create(**validated_data)
        for idx, text in enumerate(options):
            Option.objects.create(poll=poll, text=text.strip(), order=idx)
        return poll


class PollDetailSerializer(serializers.ModelSerializer):
    # map `title` -> `question` for frontend compatibility
    question = serializers.CharField(source='title')
    options = OptionSerializer(many=True, read_only=True)
    totalVotes = serializers.SerializerMethodField()
    hasVoted = serializers.SerializerMethodField()
    createdBy = serializers.SerializerMethodField()
    createdByUser = serializers.SerializerMethodField()
    views = serializers.IntegerField(source='views')
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')
    expiresAt = serializers.DateTimeField(source='expires_at', allow_null=True)
    isActive = serializers.BooleanField(source='is_active')

    class Meta:
        model = Poll
        fields = (
            'id', 'question', 'description', 'createdAt', 'updatedAt', 'expiresAt', 'isActive',
            'options', 'totalVotes', 'hasVoted', 'views', 'createdBy', 'createdByUser'
        )


class PollListSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='title')
    createdAt = serializers.DateTimeField(source='created_at')
    totalVotes = serializers.SerializerMethodField()
    createdBy = serializers.SerializerMethodField()
    isActive = serializers.BooleanField(source='is_active')

    class Meta:
        model = Poll
        fields = ('id', 'question', 'createdAt', 'isActive', 'totalVotes', 'views', 'createdBy')

    def get_totalVotes(self, obj):
        return Vote.objects.filter(poll=obj).count()

    def get_createdBy(self, obj):
        return str(obj.created_by.id) if obj.created_by else None

    def get_totalVotes(self, obj):
        # efficient count across options
        return Vote.objects.filter(poll=obj).count()

    def get_hasVoted(self, obj):
        voter_id = self.context.get('voter_id')
        if not voter_id and self.context.get('request') and getattr(self.context['request'], 'user', None) and self.context['request'].user.is_authenticated:
            voter_id = str(self.context['request'].user.id)
        if not voter_id:
            return False
        return Vote.objects.filter(poll=obj, voter_id=voter_id).exists()

    def get_createdBy(self, obj):
        return str(obj.created_by.id) if obj.created_by else None

    def get_createdByUser(self, obj):
        if not obj.created_by:
            return None
        return {
            'id': str(obj.created_by.id),
            'name': getattr(obj.created_by, 'name', getattr(obj.created_by, 'get_full_name', lambda: getattr(obj.created_by, 'email', ''))()),
            'email': getattr(obj.created_by, 'email', None),
            'avatar': getattr(obj.created_by, 'avatar', None),
            'createdAt': obj.created_by.created_at if hasattr(obj.created_by, 'created_at') else None,
            'updatedAt': obj.created_by.updated_at if hasattr(obj.created_by, 'updated_at') else None,
        }


class VoteSerializer(serializers.ModelSerializer):
    # frontend names: pollId, optionId, userId
    pollId = serializers.UUIDField(write_only=True)
    optionId = serializers.UUIDField(write_only=True)
    userId = serializers.CharField(write_only=True, required=False, allow_null=True)

    id = serializers.UUIDField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'pollId', 'optionId', 'userId', 'createdAt')

    def validate(self, attrs):
        poll_id = attrs.get('pollId')
        option_id = attrs.get('optionId')
        voter = attrs.get('userId')
        # if no explicit userId provided, try to use authenticated user from context
        if not voter:
            request = self.context.get('request')
            if request and getattr(request, 'user', None) and request.user.is_authenticated:
                voter = str(request.user.id)

        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            raise serializers.ValidationError('Poll does not exist')

        try:
            option = Option.objects.get(id=option_id)
        except Option.DoesNotExist:
            raise serializers.ValidationError('Option does not exist')

        if poll.has_expired():
            raise serializers.ValidationError('Poll has expired')

        if option.poll_id != poll.id:
            raise serializers.ValidationError('Option does not belong to the poll')

        if Vote.objects.filter(poll=poll, voter_id=voter).exists():
            raise serializers.ValidationError('Voter has already voted on this poll')

        # attach resolved objects for create()
        attrs['poll'] = poll
        attrs['option'] = option
        attrs['voter_id'] = voter
        return attrs

    def create(self, validated_data):
        poll = validated_data['poll']
        option = validated_data['option']
        voter = validated_data['voter_id']
        vote = Vote.objects.create(poll=poll, option=option, voter_id=voter)
        return vote
