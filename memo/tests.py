import factory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .forms import MemoSearchForm
from .models import Memo


# Create your tests here.

class MemoFactory(factory.django.DjangoModelFactory):
    """Create data for the Memo model used for tests"""
    title = 'Example memo'
    slug = 'example-memo'
    text = 'This is an example memo.'
    created_datetime = timezone.now()
    updated_datetime = timezone.now()

    class Meta:
        model = Memo


# Tests for the forms

class MemoSearchFormTests(TestCase):

    def test_filter_memos(self):
        memo_1 = MemoFactory(
            title='First memo', slug='first-memo', text='This memo is opened.'
        )
        memo_2 = MemoFactory(
            title='Second memo', slug='second-memo', text='This is the second memo.'
        )
        memo_3 = MemoFactory(
            title='Third memo', slug='third-memo', text='This is not the first memo.'
        )
        memo_4 = MemoFactory(
            title='Dummy first memo', slug='forth-memo', text='This is the forth memo.'
        )
        memo_5 = MemoFactory(
            title='Draft memo', slug='fifth-memo', text='The First memo has been withdrawn.'
        )
        form = MemoSearchForm({'keyword': 'first'})
        memos = form.filter_memos(Memo.objects.all())
        self.assertEqual(Memo.objects.count(), 5)
        self.assertEqual(memos.count(), 4)
        self.assertEqual(memos[0].text, 'The First memo has been withdrawn.')
        self.assertEqual(memos[1].title, 'Dummy first memo')
        self.assertEqual(memos[2].text, 'This is not the first memo.')
        self.assertEqual(memos[3].title, 'First memo')

    def test_not_filter_memos(self):
        memo_1 = MemoFactory(slug='first-memo')
        memo_2 = MemoFactory(slug='second-memo')
        form = MemoSearchForm({'keyword': ''})
        memos = form.filter_memos(Memo.objects.all())
        self.assertEqual(Memo.objects.count(), 2)
        self.assertEqual(memos.count(), 2)


# Tests for the views

class MemoListTests(TestCase):

    def test_get_memo_list(self):
        memo_1 = MemoFactory(title='First memo', slug='first-memo')
        memo_2 = MemoFactory(title='Second memo', slug='second-memo')
        res = self.client.get(reverse('memo:index'))
        self.assertTemplateUsed(res, 'memo/index.html')
        self.assertQuerysetEqual(
            res.context['memo_list'],
            ['<Memo: Second memo>', '<Memo: First memo>']
        )

    def test_get_empty_memo_list(self):
        res = self.client.get(reverse('memo:index'))
        self.assertTemplateUsed(res, 'memo/index.html')
        self.assertContains(res, '表示するメモがありません。')
        self.assertQuerysetEqual(
            res.context['memo_list'],
            []
        )

    def get_paginate(self):
        memo_1 = MemoFactory(
            title='Memo 1',
            slug='memo-1'
        )
        memo_2 = MemoFactory(
            title='Memo 2',
            slug='memo-2'
        )
        memo_3 = MemoFactory(
            title='Memo 3',
            slug='memo-3'
        )
        memo_4 = MemoFactory(
            title='Memo 4',
            slug='memo-4'
        )
        memo_5 = MemoFactory(
            title='Memo 5',
            slug='memo-5'
        )
        memo_6 = MemoFactory(
            title='Memo 6',
            slug='memo-6'
        )
        memo_7 = MemoFactory(
            title='Memo 7',
            slug='memo-7'
        )
        memo_8 = MemoFactory(
            title='Memo 8',
            slug='memo-8'
        )
        memo_9 = MemoFactory(
            title='Memo 9',
            slug='memo-9'
        )
        memo_10 = MemoFactory(
            title='Memo 10',
            slug='memo-10'
        )
        memo_11 = MemoFactory(
            title='Memo 11',
            slug='memo-11'
        )
        res_page_1 = self.client.get(reverse('memo:index'), data={'page': 1})
        res_page_2 = self.client.get(reverse('memo:index'), data={'page': 2})
        self.assertTemplateUsed(res_page_1, 'memo/index.html')
        self.assertTemplateUsed(res_page_2, 'memo/index.html')
        self.assertEqual(Memo.objects.count(), 11)
        self.assertQuerysetEqual(
            res_page_1.context['memo_list'],
            [
                '<Memo: Memo 11>',
                '<Memo: Memo 10>',
                '<Memo: Memo 9>',
                '<Memo: Memo 8>',
                '<Memo: Memo 7>',
                '<Memo: Memo 6>',
                '<Memo: Memo 5>',
                '<Memo: Memo 4>',
                '<Memo: Memo 3>',
                '<Memo: Memo 2>',
            ]
        )
        self.assertQuerysetEqual(
            res_page_2.context['memo_list'],
            ['<Memo: Memo 1>']
        )

    def get_non_existent_page_number(self):
        memo = MemoFactory()
        res = self.client.get(reverse('memo:index'), data={'page': 2})
        self.assertEqual(res.status_code, 404)

    def get_string_page_number(self):
        memo = Memofactory()
        res = self.client.get(reverse('memo:index'), data={'page': 'string'})
        self.assertEqual(res.status_code, 404)


class MemoDetailTests(TestCase):

    def test_get_memo(self):
        memo = MemoFactory(title='Sample memo', slug='sample-memo')
        res = self.client.get(reverse('memo:detail', kwargs={'slug': 'sample-memo'}))
        self.assertTemplateUsed(res, 'memo/detail.html')
        self.assertEqual(res.context['memo'].title, 'Sample memo')

    def test_get_non_existent_memo(self):
        res = self.client.get(reverse('memo:detail', kwargs={'slug': 'memo'}))
        self.assertEqual(res.status_code, 404)


class MemoCreateTests(TestCase):

    def test_get_create_form(self):
        res = self.client.get(reverse('memo:new_memo'))
        self.assertTemplateUsed('memo/new.html')

    def test_create_new_memo(self):
        new_memo = {
            'title': 'New memo',
            'slug': 'new-memo',
            'text': 'This is a new memo.'
        }
        res = self.client.post(reverse('memo:new_memo'), data=new_memo)
        self.assertRedirects(res, reverse('memo:index'))
        self.assertEqual(Memo.objects.count(), 1)

    def test_create_empty_memo(self):
        new_memo = {'title': 'Sample memo', 'slug': 'sample-memo', 'text': ''}
        res = self.client.post(reverse('memo:new_memo'), data=new_memo)
        self.assertEqual(Memo.objects.count(), 0)


class MemoDeleteTests(TestCase):

    def test_get_delete_page(self):
        memo = MemoFactory(slug='sample-memo')
        res = self.client.get(reverse('memo:delete_memo', kwargs={'slug': 'sample-memo'}))
        self.assertTemplateUsed(res, 'memo/delete.html')

    def test_delete_memo(self):
        memo = MemoFactory(slug='sample-memo')
        res = self.client.post(reverse('memo:delete_memo', kwargs={'slug': 'sample-memo'}))
        self.assertRedirects(res, reverse('memo:index'))
        self.assertEqual(Memo.objects.count(), 0)

    def test_delete_non_existent_memo(self):
        res = self.client.post(reverse('memo:delete_memo', kwargs={'slug': 'sample-memo'}))
        self.assertEqual(res.status_code, 404)


class MemoUpdateTests(TestCase):

    def test_get_update_form(self):
        memo = MemoFactory(slug='sample-memo')
        res = self.client.get(reverse('memo:edit_memo', kwargs={'slug': 'sample-memo'}))
        self.assertTemplateUsed(res, 'memo/edit.html')

    def test_get_non_existent_memo_form(self):
        res = self.client.get(reverse('memo:edit_memo', kwargs={'slug': 'sample-memo'}))
        self.assertEqual(res.status_code, 404)

    def test_update_memo(self):
        memo = MemoFactory(title='Sample', slug='sample-memo', text='This is a sample memo.')
        updated_memo = {'title': 'Sample', 'slug': 'sample-memo', 'text': 'This text is updated.'}
        res = self.client.post(reverse('memo:edit_memo', kwargs={'slug': 'sample-memo'}), data=updated_memo)
        self.assertRedirects(res, reverse('memo:index'))
        memo.refresh_from_db()
        self.assertEqual(Memo.objects.count(), 1)
        self.assertEqual(memo.text, 'This text is updated.')

    def test_update_non_existent_memo(self):
        res = self.client.post(reverse('memo:edit_memo', kwargs={'slug': 'sample'}))
        self.assertEqual(res.status_code, 404)


class MemoListAPITests(APITestCase):

    def test_get_memos_api(self):
        memo_1 = MemoFactory(title='first memo', slug='first-memo')
        memo_2 = MemoFactory(title='second-memo', slug='second-memo')
        res = self.client.get(reverse('memo:api_list'), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Memo.objects.count(), 2)


class MemoRetrieveAPITests(APITestCase):

    def test_get_memo_api(self):
        memo = MemoFactory(title='Sample memo', slug='sample-memo')
        res = self.client.get(reverse('memo:api_retrieve', kwargs={'slug': 'sample-memo'}), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_404_api(self):
        res = self.client.get(reverse('memo:api_retrieve', kwargs={'slug': 'sample-memo'}), format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class MemoCreateAPITests(APITestCase):

    def test_post_api(self):
        new_memo = {
            'title': 'New memo',
            'slug': 'new-memo',
            'text': 'This is a new memo.'
        }
        res = self.client.post(reverse('memo:api_create'), data=new_memo)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Memo.objects.count(), 1)

    def test_post_invalid_api(self):
        new_memo = {
            'title': '',
            'slug': 'new-memo',
            'text': 'This is a new memo.'
        }
        res = self.client.post(reverse('memo:api_create'), data=new_memo)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Memo.objects.count(), 0)


class MemoUpdateAPITests(APITestCase):

    def test_put_api(self):
        memo = MemoFactory(title='Sample memo', slug='sample-memo', text='This is a sample memo.')
        updated_memo = {'title': 'Sample memo', 'slug': 'sample-memo', 'text': 'This text is updated.'}
        res = self.client.put(reverse('memo:api_update', kwargs={'slug': 'sample-memo'}), data=updated_memo)
        memo.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Memo.objects.count(), 1)
        self.assertEqual(memo.text, 'This text is updated.')

    def test_put_invalid_api(self):
        memo = MemoFactory(title='Sample memo', slug='sample-memo', text='This is a sample memo.')
        updated_memo = {'title': '', 'slug': 'sample-memo', 'text': 'This text is updated.'}
        res = self.client.put(reverse('memo:api_update', kwargs={'slug': 'sample-memo'}), data=updated_memo)
        memo.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Memo.objects.count(), 1)
        self.assertEqual(memo.text, 'This is a sample memo.')


class MemoDestroyAPITests(APITestCase):

    def test_delete_api(self):
        memo = MemoFactory(title='Sample', slug='sample-memo', text='This is a sample memo.')
        res = self.client.delete(reverse('memo:api_delete', kwargs={'slug': 'sample-memo'}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Memo.objects.count(), 0)

    def test_delete_invalid_api(self):
        res = self.client.delete(reverse('memo:api_delete', kwargs={'slug': 'sample-memo'}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
