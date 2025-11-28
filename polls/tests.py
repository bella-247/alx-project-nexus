from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from .models import Poll, Option, Vote
import uuid


class PollsAPITestCase(APITestCase):
    def setUp(self):
        self.create_url = reverse('poll-create')
        self.vote_url = reverse('vote-create')

    def test_create_poll_with_options(self):
        payload = {
            'title': 'Favorite color',
            'description': 'Choose a color',
            'options': ['Red', 'Blue', 'Green']
        }
        resp = self.client.post(self.create_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        poll_id = resp.data.get('id')
        self.assertIsNotNone(poll_id)
        poll = Poll.objects.get(id=poll_id)
        self.assertEqual(poll.options.count(), 3)

    def test_vote_and_prevent_duplicate(self):
        poll = Poll.objects.create(title='Test', description='t')
        opt = Option.objects.create(poll=poll, text='Yes')

        payload = {'poll': str(poll.id), 'option': str(opt.id), 'voter_id': 'user-1'}
        resp = self.client.post(self.vote_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # duplicate vote attempt
        resp2 = self.client.post(self.vote_url, payload, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_results_count(self):
        poll = Poll.objects.create(title='Count Test')
        o1 = Option.objects.create(poll=poll, text='A')
        o2 = Option.objects.create(poll=poll, text='B')
        Vote.objects.create(poll=poll, option=o1, voter_id='u1')
        Vote.objects.create(poll=poll, option=o1, voter_id='u2')
        Vote.objects.create(poll=poll, option=o2, voter_id='u3')

        url = reverse('poll-results', kwargs={'pk': poll.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.data
        self.assertEqual(data['total_votes'], 3)
        results = {r['text']: r['votes'] for r in data['results']}
        self.assertEqual(results.get('A'), 2)
        self.assertEqual(results.get('B'), 1)
