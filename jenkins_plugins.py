import requests


PLUGIN_DIRECTORY = '/var/lib/jenkins'  # With paths
CACHE = {}


class Plugin(object):

    def __init__(self, name):
        self._name = name

    def download(self):
        response = requests.get(self._plugin_url)
        with open(self._plugin_file, 'wb') as file:
            file.write(response.content)

    def get_dependencies(self):
        # parse META-INF/MANIFEST.MF
        # parse 'Plugin-Dependencies:'
        pass

    @property
    def _plugin_url(self):
        url_pattern = "https://updates.jenkins-ci.org/latest/{name}.hpi"
        return url_pattern.format(name=self._name)

    @property
    def _plugin_file(self):
        return PLUGIN_DIRECTORY + '/{name}.hpi'.format(name=self._name)
