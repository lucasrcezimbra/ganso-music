import eyed3
import os.path
from django.test import TestCase
from gansomusic.core.forms import MusicForm
from gansomusic.core.views import get_filename
from gansomusic.core.helpers import Mp3Tagger
from pydub.utils import mediainfo
from unittest.mock import Mock
from urllib.parse import quote
from shutil import copyfile

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
        content_disposition = "attachment; filename*=utf-8''{}"\
                                .format(quote(filename))
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
        mp3 = eyed3.load(response_file)
        self.assertIsNotNone(mp3.tag.lyrics)

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

        expected_filename = 'MENOR VIDEO DO MUNDO! THE BIGGER VIDEO IN THE WORLD!.mp3'
        content_disposition = "attachment; filename*=utf-8''{}"\
                                .format(quote(expected_filename))
        self.assertEquals(content_disposition,
                          self.response.get('Content-Disposition'))

    def test_get_filename(self):
        youtube_title = 'Youtube Title'

        self.assertEqual(get_filename('title', 'artist', youtube_title),
                         'artist - title.mp3')
        self.assertEqual(get_filename('', 'artist', youtube_title),
                         '{}.mp3'.format(youtube_title))
        self.assertEqual(get_filename('title', '', youtube_title),
                         '{}.mp3'.format(youtube_title))
        self.assertEqual(get_filename('', '', youtube_title),
                         '{}.mp3'.format(youtube_title))

    def test_id3_version(self):
        response_file = self.response_to_file()
        mp3 = eyed3.load(response_file)
        self.assertEqual(mp3.tag.version, (2,3,0))

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

class Mp3TaggerHelperTest(TestCase):
    def setUp(self):
        self.tests_path = os.path.dirname(os.path.realpath(__file__))
        self.path = self.tests_path + '/audio.mp3'

        self._create_new_audiofile()

        self.title = 'Back in Black'
        self.artist = 'AC/DC'
        self.genre = 'Rock'
        self.mp3_tagger = Mp3Tagger(self.path, self.title,
                                    self.artist, self.genre)

    def test_init_mp3_tagger(self):
        self.assertEqual(self.mp3_tagger.path, self.path)
        self.assertEqual(self.mp3_tagger.title, self.title)
        self.assertEqual(self.mp3_tagger.artist, self.artist)
        self.assertEqual(self.mp3_tagger.genre, self.genre)
        self.assertEqual(self.mp3_tagger.id3_version, eyed3.id3.ID3_V2_3)

    def test_edit_tags(self):
        self.mp3_tagger.edit_tags()
        id3_tag = eyed3.load(self.mp3_tagger.path).tag
        self.assertEqual(id3_tag.title, self.mp3_tagger.title)
        self.assertEqual(id3_tag.artist, self.mp3_tagger.artist)
        self.assertEqual(id3_tag.genre.name, self.mp3_tagger.genre)
        self.assertEqual(id3_tag.version, self.mp3_tagger.id3_version)

    def test_lyric_tag(self):
        self.mp3_tagger.edit_tags()
        id3_tag = eyed3.load(self.mp3_tagger.path).tag
        self.assertTrue(id3_tag.lyrics[0].text)

    def tearDown(self):
        os.remove(self.path)

    def _create_new_audiofile(self):
        audio_without_tags_path = self.tests_path + '/audio_without_tags.mp3'
        copyfile(audio_without_tags_path, self.path)
