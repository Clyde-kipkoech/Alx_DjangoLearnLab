from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.other = User.objects.create_user(username='u2', password='pass12345')
        self.post = Post.objects.create(title='A', content='content', author=self.user)

    def test_create_comment_requires_login(self):
        url = reverse('comment_create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Nice post!'})
        # should redirect to login
        self.assertNotEqual(resp.status_code, 200)

        # login and create
        self.client.login(username='u1', password='pass12345')
        resp = self.client.post(url, {'content': 'Nice post!'})
        self.assertEqual(resp.status_code, 302)  # redirect to post detail
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.user, content='Nice post!').exists())

    def test_edit_comment_by_author_only(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='hello')
        url = reverse('comment_update', kwargs={'post_pk': self.post.pk, 'pk': comment.pk})
        # other user cannot edit
        self.client.login(username='u2', password='pass12345')
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)  # should be forbidden or redirect
        # author can edit
        self.client.login(username='u1', password='pass12345')
        resp = self.client.post(url, {'content': 'edited'})
        self.assertEqual(resp.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'edited')

    def test_delete_comment_by_author_only(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='delme')
        url = reverse('comment_delete', kwargs={'post_pk': self.post.pk, 'pk': comment.pk})
        self.client.login(username='u2', password='pass12345')
        resp = self.client.post(url)
        self.assertNotEqual(resp.status_code, 302)  # not allowed
        self.client.login(username='u1', password='pass12345')
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
