from django.contrib.messages.context_processors import messages
from django.template.defaultfilters import first
from django.test import TestCase
from store.models import Category, Author, Publisher
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from store.views import about


class CategoryTestCase(TestCase):
    def test_create_category(self):
        category = Category.objects.create(
            name='Test'
        )
        self.assertEqual(str(category), 'Test')
        self.assertTrue(isinstance(category, Category))

    def test_category_name_max_length(self):
        category = Category(name='A' * 101)
        with self.assertRaises(ValidationError):
            category.full_clean()


    def test_category_name_not_empty(self):
        category = Category(name='')
        with self.assertRaises(ValidationError):
            category.full_clean()



class AuthorTestCase(TestCase):
    def test_create_author(self):
        author = Author.objects.create(
            first_name='Peter',
            last_name='Smith',
            social_media='',
            picture=''
        )

        self.assertEqual(author.first_name, 'Peter')
        self.assertEqual(author.last_name, 'Smith')
        self.assertEqual(str(author), 'Peter Smith')
        self.assertTrue(isinstance(author, Author))

    def test_names_max_length(self):
        author = Author(
            first_name='Peter',
            last_name='S' * 71
        )
        author_2 = Author(
            first_name = 'P' * 51,
            last_name = 'Smith'
        )

        with self.assertRaises(ValidationError):
            author.full_clean()

        with self.assertRaises(ValidationError):
            author_2.full_clean()


    def test_names_not_empty(self):
        author = Author(
            first_name='Peter',
            last_name=''
        )
        author_2 = Author(
            first_name='',
            last_name='Smith'
        )

        with self.assertRaises(ValidationError):
            author.full_clean()

        with self.assertRaises(ValidationError):
            author_2.full_clean()

    # def test_image_uploader(self):
    #     author_picture = SimpleUploadedFile('author.jpg', b'file data')
    #     author = Author.objects.create(
    #             first_name='Ali',
    #             last_name='Hazelwood',
    #             picture=author_picture
    #         )
    #     self.assertTrue(author.picture.name.startswith('author/'))


class PublisherTestCase(TestCase):
    def test_create_publisher(self):
        publisher = Publisher.objects.create(
            name='Test'
        )
        self.assertEqual(str(publisher), 'Test')
        self.assertTrue(isinstance(publisher, Publisher))

    def test_publisher_name_max_length(self):
        publisher = Publisher(name='A' * 61)
        with self.assertRaises(ValidationError):
            publisher.full_clean()


    def test_publisher_name_not_empty(self):
        publisher = Publisher(name='')
        with self.assertRaises(ValidationError):
            publisher.full_clean()
