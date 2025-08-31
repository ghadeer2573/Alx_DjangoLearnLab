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
