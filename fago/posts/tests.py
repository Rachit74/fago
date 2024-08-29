from django.test import TestCase
from .models import Post, Comment

from django.contrib.auth.models import User


# Create your tests here

class CommentTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', password='1234')
        user2 = User.objects.create(username='user2', password='1234')
        post = Post.objects.create(title='Test Post', author=user1, content='The Content')

        self.parent_comment = Comment.objects.create(comment='Parent comment', comment_author=user1, post=post)

        self.sub_comment = Comment.objects.create(comment='Child Comment', comment_author=user2, post=post, parent_comment=self.parent_comment)

    def test_is_parent(self):
        self.assertTrue(self.parent_comment.is_parent())
        self.assertFalse(self.sub_comment.is_parent())