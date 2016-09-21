import unittest
import jenkins_plugins
import os.path
from httmock import urlmatch, HTTMock


class TestPlugin(unittest.TestCase):

    def setUp(self):
        jenkins_plugins.PLUGIN_DIRECTORY = '/tmp'
        self._name = 'fake-name'
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
            file_name = 'dependencies.hpi'
        else:
            file_name = 'no_dependencies.hpi'
        return self._read_hpi(file_name)

    def _read_hpi(self, file_name):
        root_folder = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(root_folder, 'fixtures', file_name)
        with open(file_path, 'br') as file:
            return file.read()

    def _delete_plugins(self):
        for plugin_path in self._plugin_paths:
            try:
                os.remove(plugin_path)
            except OSError:
                pass

    @property
    def _plugins(self):
        # Fake-name plugin along with its dependencies
        return ['fake-name', 'credentials', 'durable-task']

    @property
    def _plugin_paths(self):
        return ['/tmp/{file}.hpi'.format(file=x) for x in self._plugins]


class TestManifest(unittest.TestCase):

    def test_dependencies(self):
        file_path = os.path.join(self._fixtures_folder, 'dependencies.hpi')
        manifest = jenkins_plugins.Manifest(file_path)
        dependencies = ['credentials', 'durable-task']
        self.assertListEqual(dependencies, manifest.dependencies)

    def test_no_dependencies(self):
        file_path = os.path.join(self._fixtures_folder, 'no_dependencies.hpi')
        manifest = jenkins_plugins.Manifest(file_path)
        self.assertListEqual([], manifest.dependencies)

    @property
    def _fixtures_folder(self):
        root_folder = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(root_folder, 'fixtures')

if __name__ == '__main__':
    unittest.main()
