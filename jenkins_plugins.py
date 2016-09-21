import requests
import zipfile
import re
import os.path

#PLUGIN_DIRECTORY = '/var/lib/jenkins'  # With paths
PLUGIN_DIRECTORY = '/home/chmelda/jenkins'  # With paths


class Plugin(object):

    def __init__(self, name):
        self._name = name

    def download(self):
        if self._plugin_exists:
            return self
        response = requests.get(self._plugin_url)
        self._save_plugin(response)
        self._get_dependencies()

    def _get_dependencies(self):
        for dependency in Manifest(self._plugin_file).dependencies:
            Plugin(dependency).download()

    def _save_plugin(self, response):
        with open(self._plugin_file, 'wb') as file:
            file.write(response.content)
        print('Downloaded plugin {plugin}'.format(plugin=self._name))

    @property
    def _plugin_exists(self):
        if os.path.isfile(self._plugin_file):
            print('Skipping plugin {plugin}, already installed.'.format(plugin=self._name))
            return True
        return False


    @property
    def _plugin_url(self):
        url_pattern = "https://updates.jenkins-ci.org/latest/{name}.hpi"
        return url_pattern.format(name=self._name)

    @property
    def _plugin_file(self):
        return PLUGIN_DIRECTORY + '/{name}.hpi'.format(name=self._name)


class Manifest(object):

    def __init__(self, plugin_file):
        self._plugin_file = plugin_file

    @property
    def dependencies(self):
        for line in self._load_manifest():
            regex = re.search(b"^Plugin-Dependencies: (.*)", line)
            if regex:
                return [x.split(':')[0] for x in regex.group(1).decode('ascii').split(',')]
        return []

    def _load_manifest(self):
        with zipfile.ZipFile(self._plugin_file) as zip_file:
             with zip_file.open('META-INF/MANIFEST.MF', 'r') as manifest_file:
                 for line in manifest_file:
                     yield line
