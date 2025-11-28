from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from polls.models import Poll, Option, Vote


class AuthVoteFlowTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.polls_url = reverse('poll-list-create')
        self.votes_url = reverse('vote-create')

    def test_register_login_create_poll_and_vote(self):
        # register
        reg_data = {'email': 'a@example.com', 'name': 'Alice', 'password': 'strongpass'}
        r = self.client.post(self.register_url, reg_data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        # login
        r = self.client.post(self.login_url, {'email': 'a@example.com', 'password': 'strongpass'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        token = r.data.get('access')
        self.assertIsNotNone(token)

        auth = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        # create poll
        poll_payload = {'question': 'Q?', 'description': 'desc', 'options': ['x', 'y']}
        r = self.client.post(self.polls_url, poll_payload, format='json', **auth)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        poll_id = r.data.get('id')
        # fetch options
        poll = Poll.objects.get(id=poll_id)
        option = poll.options.first()

        # vote
        vote_payload = {'pollId': str(poll.id), 'optionId': str(option.id)}
        r = self.client.post(self.votes_url, vote_payload, format='json', **auth)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
