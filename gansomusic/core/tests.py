import os.path
from django.test import TestCase
from gansomusic.core.forms import MusicForm

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get_index(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_index(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_has_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 7),
                ('type="text"', 4),
                ('type="reset"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

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

    def test_response_content_disposition(self):
        content_disposition = 'attachment; filename={}'.format(self.filename)
        self.assertEquals(content_disposition, self.response.get('Content-Disposition'))

    def test_response_content_type_is_mp3(self):
        content_type = 'audio/mpeg3'
        self.assertEquals(content_type, self.response.get('Content-Type'))

    def test_content_is_not_none(self):
        self.assertTrue(self.response.content)


class MusicFormTest(TestCase):
    def test_form_has_fields(self):
        form = MusicForm()
        expected = ['url', 'title', 'artist', 'gender']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_url_is_required(self):
        form = self.make_validated_form(url='')
        self.assertFormErrorMessage(form, 'url', 'Este campo é obrigatório.')

    def make_validated_form(self, **kwargs):
        valid = dict(url='wJM-eaC8mug', title='Titulo',
                     artist='Artista1', gender='Rock')
        data = dict(valid, **kwargs)
        form = MusicForm(data)
        form.is_valid()
        return form

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertEqual([msg], errors_list)
