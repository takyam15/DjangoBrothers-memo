import factory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import MemoSearchForm
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
        self.assertTemplateUsed(res, 'memo/detail.html')
        self.assertEqual(res.context['memo'].title, 'Example memo')

    def test_404(self):
        res = self.client.get(reverse('memo:detail', kwargs={'slug': 'memo'}))
        self.assertEqual(res.status_code, 404)


class MemoCreateTests(TestCase):
    def test_get(self):
        res = self.client.get(reverse('memo:new_memo'))
        self.assertTemplateUsed('memo/new.html')

    def test_post(self):
        new_memo = {'title': 'Example', 'slug': 'example', 'text': 'This is an example text.'}
        res = self.client.post(reverse('memo:new_memo'), data=new_memo)
        self.assertRedirects(res, reverse('memo:index'))
        self.assertEqual(Memo.objects.count(), 1)

    def test_empty_post(self):
        new_memo = {'title': 'Example', 'slug': 'example', 'text': ''}
        res = self.client.post(reverse('memo:new_memo'), data=new_memo)
        self.assertEqual(Memo.objects.count(), 0)


class MemoDeleteTests(TestCase):
    def test_get(self):
        memo = MemoFactory(slug='example')
        res = self.client.get(reverse('memo:delete_memo', kwargs={'slug': 'example'}))
        self.assertTemplateUsed(res, 'memo/delete.html')

    def test_post(self):
        memo = MemoFactory(slug='example')
        res = self.client.post(reverse('memo:delete_memo', kwargs={'slug': 'example'}))
        self.assertRedirects(res, reverse('memo:index'))
        self.assertEqual(Memo.objects.count(), 0)

    def test_post_404(self):
        memo = MemoFactory(slug='example')
        res = self.client.post(reverse('memo:delete_memo', kwargs={'slug': 'sample'}))
        self.assertEqual(res.status_code, 404)


class MemoUpdateTests(TestCase):
    def test_get(self):
        memo = MemoFactory(slug='example')
        res = self.client.get(reverse('memo:edit_memo', kwargs={'slug': 'example'}))
        self.assertTemplateUsed(res, 'memo/edit.html')

    def test_post(self):
        memo = MemoFactory(title='Example', slug='example', text='This is an example text.')
        updated_memo = {'title': 'Example', 'slug': 'example', 'text': 'This text is updated.'}
        res = self.client.post(reverse('memo:edit_memo', kwargs={'slug': 'example'}), data=updated_memo)
        self.assertRedirects(res, reverse('memo:detail', kwargs={'slug': 'example'}))
        memo.refresh_from_db()
        self.assertEqual(memo.text, 'This text is updated.')

    def test_post_404(self):
        memo = MemoFactory(title='Example', slug='example', text='This is an example text.')
        res = self.client.post(reverse('memo:edit_memo', kwargs={'slug': 'sample'}))
        self.assertEqual(res.status_code, 404)
