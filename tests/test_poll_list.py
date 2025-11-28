from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from polls.models import Poll, Option


class PollListTests(APITestCase):
    def setUp(self):
        # create a few polls
        for i in range(3):
            p = Poll.objects.create(title=f'Poll {i}', description='desc')
            Option.objects.create(poll=p, text='A')

    def test_list_polls_wrapped(self):
        url = reverse('poll-list-create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('polls', resp.data)
        self.assertIsInstance(resp.data['polls'], list)
        self.assertGreaterEqual(len(resp.data['polls']), 3)
