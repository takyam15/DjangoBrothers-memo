import factory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Memo


# Create your tests here.

class MemoFactory(factory.django.DjangoModelFactory):
    """Create data for the Memo model used for tests"""
    title = 'Example title'
    slug = 'example-slug'
    text = 'This is an example text.'
    created_datetime = timezone.now()
    updated_datetime = timezone.now()

    class Meta:
        model = Memo


# Tests for the views

class MemoListTests(TestCase):
    def test_get_single_memo(self):
        memo = MemoFactory(title='Single memo')
        res = self.client.get(reverse('memo:index'))
        self.assertTemplateUsed(res, 'memo/index.html')
        self.assertQuerysetEqual(
            res.context['memo_list'],
            ['<Memo: Single memo>']
        )

    def test_get_two_memos(self):
        memo_1 = MemoFactory(title='First memo', slug='first-memo')
        memo_2 = MemoFactory(title='Second memo', slug='second-memo')
        res = self.client.get(reverse('memo:index'))
        self.assertTemplateUsed(res, 'memo/index.html')
        self.assertQuerysetEqual(
            res.context['memo_list'],
            ['<Memo: Second memo>', '<Memo: First memo>']
        )

    def test_get_empty_memo(self):
        res = self.client.get(reverse('memo:index'))
        self.assertTemplateUsed(res, 'memo/index.html')
        self.assertContains(res, '表示するメモがありません。')
        self.assertQuerysetEqual(
            res.context['memo_list'],
            []
        )


class MemoDetailTests(TestCase):
    def test_get(self):
        memo = MemoFactory(title='Example memo', slug='memo')
        res = self.client.get(reverse('memo:detail', kwargs={'slug': 'memo'}))
        self.assertTemplateUsed()
        self.assertEqual(res.context['memo'].title, 'Example memo')

    def test_404(self):
        res = self.client.get(reverse('memo:detail', kwargs={'slug': 'memo'}))
        self.assertEqual(res.status_code, 404)