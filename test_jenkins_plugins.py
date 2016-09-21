import unittest
import jenkins_plugins
import os.path
from httmock import urlmatch, HTTMock


class TestPlugin(unittest.TestCase):

    def setUp(self):
        jenkins_plugins.PLUGIN_DIRECTORY = '/tmp'
        self._name = 'fake-name'
        self._fake_content = 'fake content'
        self._delete_plugins()

    def tearDown(self):
        self._delete_plugins()

    def test_download(self):
        plugin = jenkins_plugins.Plugin(self._name)
        with HTTMock(self._jenkins_mock):
            plugin.download()
        for plugin_path in self._plugin_paths:
            self.assertTrue(os.path.exists(plugin_path))

    @urlmatch(netloc=r'(.*\.)?jenkins-ci\.org$')
    def _jenkins_mock(self, url, request):
        if url[2] == '/latest/{name}.hpi'.format(name=self._name):
            file_path = os.path.dirname(os.path.realpath(__file__)) + '/fixtures/dependencies.hpi'
        else:
            file_path = os.path.dirname(os.path.realpath(__file__)) + '/fixtures/no_dependencies.hpi'
        with open(file_path, 'br') as file:
            return file.read()

    def _delete_plugins(self):
        for plugin_path in self._plugin_paths:
            try:
                os.remove(plugin_path)
            except OSError:
                pass

    @property
    def _plugin_paths(self):
        return ['/tmp/{file}.hpi'.format(file=x) for x in ['fake-name', 'credentials', 'durable-task']]


class TestManifest(unittest.TestCase):

    def test_dependencies(self):
        fixtures_folder = os.path.dirname(os.path.realpath(__file__)) + '/fixtures/'
        self.assertListEqual(['credentials', 'durable-task'], jenkins_plugins.Manifest(fixtures_folder + 'dependencies.hpi').dependencies)
        self.assertListEqual([], jenkins_plugins.Manifest(fixtures_folder + 'no_dependencies.hpi').dependencies)

if __name__ == '__main__':
    unittest.main()
