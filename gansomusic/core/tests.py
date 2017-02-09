from django.test import TestCase

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get_index(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_index(self):
        self.assertTemplateUsed(self.response, 'index.html')
