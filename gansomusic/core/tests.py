import os.path
from django.test import TestCase

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get_index(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_index(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_has_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

class DownloadTest(TestCase):
    def setUp(self):
        self.url = 'wJM-eaC8mug'
        self.filename = 'MENOR VIDEO DO MUNDO!_ THE BIGGER VIDEO IN THE WORLD!.m4a'
        data = dict(url=self.url)
        self.response = self.client.post('/download/', data)

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_download_file(self):
        self.assertTrue(os.path.isfile(self.filename))

    def tearDown(self):
        os.remove(self.filename)

    # def test_response_content_disposition(self):
    #     content_disposition = "attachment; filename=audio.mp3"
    #     self.assertEquals(content_disposition, self.response.get('Content-Disposition'))

    # def test_response_content_type_is_mp3(self):
    #     content_type = 'audio/mpeg3'
    #     self.assertEquals(content_type, self.response.get('Content-Type'))

    # def test_content_is_not_none(self):
    #     self.assertTrue(self.response.content)
