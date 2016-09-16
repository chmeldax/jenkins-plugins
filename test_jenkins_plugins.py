import unittest
import jenkins_plugins
from httmock import urlmatch, HTTMock


class TestPlugin(unittest.TestCase):

    def setUp(self):
        jenkins_plugins.PLUGIN_DIRECTORY = '/tmp'
        self._name = 'fake-name'
        self._fake_content = 'fake content'

    def test_download(self):
        plugin = jenkins_plugins.Plugin(self._name)
        with HTTMock(self._jenkins_mock):
            plugin.download()
        file_name = '/tmp/{file}.hpi'.format(file=self._name)
        with open(file_name, 'r') as file:
            self.assertEqual(self._fake_content, file.read())

    @urlmatch(netloc=r'(.*\.)?jenkins-ci\.org$')
    def _jenkins_mock(self, url, request):
        return self._fake_content

if __name__ == '__main__':
    unittest.main()
