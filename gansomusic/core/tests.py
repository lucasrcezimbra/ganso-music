import os.path
from django.test import TestCase
from gansomusic.core.forms import MusicForm
from gansomusic.core.views import get_filename
from pydub.utils import mediainfo

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
        self.extension = 'mp3'
        self.title = 'Music Title'
        self.artist = 'Music artist'
        self.genre = 'Music genre'
        self.filename = '{} - {}'.format(self.artist, self.title)
        self.filepath = '{}.m4a'.format(self.filename)
        data = dict(url=self.url, title=self.title,
                    artist=self.artist, genre=self.genre)
        self.response = self.client.post('/download/', data)

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_response_content_disposition(self):
        filename = '{}.{}'.format(self.filename, self.extension)
        content_disposition = 'attachment; filename={}'.format(filename)
        self.assertEquals(content_disposition,
                          self.response.get('Content-Disposition'))

    def test_response_content_type_is_mp3(self):
        content_type = 'audio/mpeg3'
        self.assertEquals(content_type, self.response.get('Content-Type'))

    def test_content_is_not_none(self):
        self.assertTrue(self.response.content)

    def test_file_is_mp3(self):
        extension = self.response.get('Content-Disposition').split('.')[-1]
        self.assertEqual('mp3', extension)

    def test_file_has_tags(self):
        response_file = self.response_to_file()
        tags = mediainfo(response_file)['TAG']
        self.assertEqual(self.title, tags.get('title'))
        self.assertEqual(self.artist, tags.get('artist'))
        self.assertEqual(self.genre, tags.get('genre'))

    def test_delete_audio_after_response(self):
        self.assertFalse(os.path.exists(self.filepath))
        self.assertFalse(os.path.exists('{}.{}'.format(self.filename,
                                                       self.extension)))
    def test_add_lyric(self):
        self.title = 'Back in Black'
        self.artist = 'AC/DC'
        data = dict(url=self.url, title=self.title,
                    artist=self.artist, genre=self.genre)
        self.response = self.client.post('/download/', data)

        response_file = self.response_to_file()
        tags = mediainfo(response_file)['TAG']
        self.assertIsNotNone(tags.get('lyrics'))

    def response_to_file(self):
        response_file = 'response_audio.mp3'

        with open(response_file, 'wb') as file:
            file.write(self.response._container[0])

        return response_file

    def test_dont_rename_when_dont_have_artist_or_title(self):
        self.title = ''
        self.artist = ''
        data = dict(url=self.url, title=self.title,
                    artist=self.artist, genre=self.genre)
        self.response = self.client.post('/download/', data)

        filename = 'MENOR VIDEO DO MUNDO! THE BIGGER VIDEO IN THE WORLD!'
        content_disposition = 'attachment; filename={}'.format(filename)
        self.assertEquals(content_disposition,
                          self.response.get('Content-Disposition'))

    def test_get_filename(self):
        youtube_title = 'Youtube Title'

        self.assertEqual(get_filename('title', 'artist', youtube_title),
                         'artist - title.mp3')
        self.assertEqual(get_filename('', 'artist', youtube_title),
                         youtube_title)
        self.assertEqual(get_filename('title', '', youtube_title),
                         youtube_title)
        self.assertEqual(get_filename('', '', youtube_title),
                         youtube_title)

    def tearDown(self):
        if os.path.exists('response_audio.mp3'):
            os.remove('response_audio.mp3')


class MusicFormTest(TestCase):
    def test_form_has_fields(self):
        form = MusicForm()
        expected = ['url', 'title', 'artist', 'genre']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_url_is_required(self):
        form = self.make_validated_form(url='')
        self.assertFormErrorMessage(form, 'url', 'Este campo é obrigatório.')

    def make_validated_form(self, **kwargs):
        valid = dict(url='wJM-eaC8mug', title='Titulo',
                     artist='Artista1', genre='Rock')
        data = dict(valid, **kwargs)
        form = MusicForm(data)
        form.is_valid()
        return form

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertEqual([msg], errors_list)
