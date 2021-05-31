import os
import stat
from conans import tools, ConanFile
from conans.errors import ConanInvalidConfiguration


class ConanLexFloatServer(ConanFile):
    name = "lexfloatserver"
    description = "LexFloatServer"
    url = "https://app.cryptlex.com/downloads"
    homepage = "https://cryptlex.com/"
    topics = ("licensing", "cryptlex")
    license = "Proprietary"
    settings = "os", "arch"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version][str(self.settings.os)])

    @property
    def _package_contents_dir(self):
        if self.settings.os == 'Linux':
            return {
                'x86_64': 'amd64',
                'armv8': 'arm64',
                'armv8.3': 'arm64',
            }[str(self.settings.arch)]

        if self.settings.os == 'Windows':
            return 'x64'

        if self.settings.os == 'Macos':
            return {
                'x86_64': 'x86_64',
                'armv8': 'arm64',
                'armv8.3': 'arm64',
            }[str(self.settings.arch)]
        raise ConanInvalidConfiguration('Libraries for this configuration are not available')

    def package(self):
        if self.settings.os != 'Windows':
            # Make executable
            server_exe = os.path.join(self._package_contents_dir, 'lexfloatserver')
            st = os.stat(server_exe)
            os.chmod(server_exe, st.st_mode | stat.S_IEXEC)
            self.copy("lexfloatserver", dst="bin", src=self._package_contents_dir)
        else:
            self.copy("LexFloatServer.exe", dst="bin", src=self._package_contents_dir)
        self.copy("config.yml", dst="share/lexfloatserver/sample", src=self._package_contents_dir)

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))

    def package_id(self):
        if self.settings.os == "Macos":
            del self.info.settings.os.version