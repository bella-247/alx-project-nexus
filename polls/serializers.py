from rest_framework import serializers
from .models import Poll, Option, Vote
from django.utils import timezone


class OptionSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Option
        fields = ('id', 'text', 'order', 'votes')


class PollCreateSerializer(serializers.ModelSerializer):
    options = serializers.ListField(child=serializers.CharField(max_length=255), write_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'expires_at', 'options')

    def validate_expires_at(self, value):
        if value is not None and value <= timezone.now():
            raise serializers.ValidationError('expires_at must be in the future')
        return value

    def create(self, validated_data):
        options = validated_data.pop('options', [])
        poll = Poll.objects.create(**validated_data)
        for idx, text in enumerate(options):
            Option.objects.create(poll=poll, text=text.strip(), order=idx)
        return poll


class PollDetailSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'created_at', 'expires_at', 'is_active', 'options')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'poll', 'option', 'voter_id', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        poll = attrs.get('poll')
        option = attrs.get('option')
        voter = attrs.get('voter_id')

        if poll.has_expired():
            raise serializers.ValidationError('Poll has expired')

        if option.poll_id != poll.id:
            raise serializers.ValidationError('Option does not belong to the poll')

        # duplicate vote check
        if Vote.objects.filter(poll=poll, voter_id=voter).exists():
            raise serializers.ValidationError('Voter has already voted on this poll')

        return attrs
