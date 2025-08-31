from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostsCommentsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass123')
        self.user2 = User.objects.create_user(username='u2', password='pass123')
        self.client = APIClient()
        self.client.login(username='u1', password='pass123')  # or use token auth

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'Hello', 'content': 'World'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)

    def test_update_post_by_non_owner(self):
        post = Post.objects.create(author=self.user, title='t', content='c')
        self.client.logout()
        self.client.login(username='u2', password='pass123')
        url = reverse('post-detail', args=[post.id])
        resp = self.client.put(url, {'title':'x','content':'y'}, format='json')
        self.assertIn(resp.status_code, [403, 405])  # must be forbidden

    def test_create_comment(self):
        post = Post.objects.create(author=self.user, title='t', content='c')
        url = reverse('comment-list')
        resp = self.client.post(url, {'post': post.id, 'content': 'nice'}, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.user)
# posts/tests.py (or a new tests_follow.py)
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user(username='alice', password='pass')
        self.b = User.objects.create_user(username='bob', password='pass')
        self.c = User.objects.create_user(username='cara', password='pass')

        # bob and cara have posts
        Post.objects.create(author=self.b, title='B1', content='bpost1')
        Post.objects.create(author=self.c, title='C1', content='cpost1')

        self.client.login(username='alice', password='pass')

    def test_follow_and_see_feed(self):
        # alice follows bob
        url = reverse('follow', kwargs={'user_id': self.b.id})
        resp = self.client.post(url)
        assert resp.status_code == 200

        # feed should now include bob's posts
        feed_url = reverse('feed')
        resp = self.client.get(feed_url)
        assert resp.status_code == 200
        data = resp.json()
        assert any(item['title'] == 'B1' for item in data['results'])

    def test_unfollow(self):
        # follow then unfollow
        self.client.post(reverse('follow', kwargs={'user_id': self.b.id}))
        self.client.post(reverse('unfollow', kwargs={'user_id': self.b.id}))
        resp = self.client.get(reverse('feed'))
        assert resp.json()['results'] == []
