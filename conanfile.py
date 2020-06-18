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
    settings = "os", "compiler", "arch"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version][str(self.settings.os)])

    @property
    def _package_contents_dir(self):
        if self.settings.os == 'Linux':
            compiler = 'gcc'
            la_arch = {
                'x86': 'i386',
                'x86_64': 'amd64',
                # TODO: map armv5el, armv5hf, armv6, armv7, armv7hf, armv7s, armv7k, armv8, armv8_32, armv8.3
                # to arm64, armel, armhf
            }[str(self.settings.arch)]
            return os.path.join(compiler, la_arch)

        if self.settings.os == 'Windows':
            la_arch = {
                'x86': 'x86',
                'x86_64': 'x64',
            }[str(self.settings.arch)]
            if self.version >= Version("4.3.2") and int(str(self.settings.compiler.version)) >= 16:
                return os.path.join('vc16', la_arch)
            else:
                return os.path.join('vc14', la_arch)

        if self.settings.os == 'Macos':
            return os.path.join('x86_64')
        raise ConanInvalidConfiguration('Libraries for this configuration are not available')

    def package(self):
        if self.settings.os != 'Windows':
            # Make executable
            server_exe = os.path.join(self._package_contents_dir, 'LexFloatServer')
            st = os.stat(server_exe)
            os.chmod(server_exe, st.st_mode | stat.S_IEXEC)
            self.copy("LexFloatServer", dst="bin", src=self._package_contents_dir)
        else:
            self.copy("LexFloatServer.exe", dst="bin", src=self._package_contents_dir)

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))

    def package_id(self):
        # we don't really care about the compiler version, unless we're on windows
        if self.settings.os != "Windows":
            self.info.settings.compiler.version = "any"