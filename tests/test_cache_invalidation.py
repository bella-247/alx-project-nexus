from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from polls.models import Poll, Option, Vote


class CacheInvalidationTests(APITestCase):
    def setUp(self):
        self.poll = Poll.objects.create(title='Cache Poll')
        self.o1 = Option.objects.create(poll=self.poll, text='A')
        self.o2 = Option.objects.create(poll=self.poll, text='B')
        self.results_url = reverse('poll-results', kwargs={'pk': self.poll.id})

    def test_results_cache_and_invalidate_on_vote(self):
        # first fetch populates cache
        r1 = self.client.get(self.results_url)
        self.assertEqual(r1.status_code, status.HTTP_200_OK)
        self.assertEqual(r1.data['totalVotes'], 0)

        # create a vote
        Vote.objects.create(poll=self.poll, option=self.o1, voter_id='u1')

        # fetch again: should reflect new vote (signals should have invalidated cache)
        r2 = self.client.get(self.results_url)
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.data['totalVotes'], 1)
