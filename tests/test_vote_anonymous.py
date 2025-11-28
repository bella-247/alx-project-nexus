from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import override_settings
from polls.models import Poll, Option


class AnonymousVoteTests(APITestCase):
    def setUp(self):
        self.poll = Poll.objects.create(title='Anon Poll')
        self.opt = Option.objects.create(poll=self.poll, text='Yes')
        self.vote_url = reverse('vote-create')

    def test_anonymous_vote_forbidden_by_default(self):
        payload = {'pollId': str(self.poll.id), 'optionId': str(self.opt.id), 'userId': 'anon-1'}
        resp = self.client.post(self.vote_url, payload, format='json')
        # without auth and ALLOW_ANONYMOUS_VOTE disabled, should be 401
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    @override_settings(ALLOW_ANONYMOUS_VOTE=True)
    def test_anonymous_vote_allowed_when_flag_set(self):
        payload = {'pollId': str(self.poll.id), 'optionId': str(self.opt.id), 'userId': 'anon-1'}
        resp = self.client.post(self.vote_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
