### Hi there š

<!--
**Faizibou/Faizibou** is a āØ _special_ āØ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- š­ Iām currently working on ...
- š± Iām currently learning ...
- šÆ Iām looking to collaborate on ...
- š¤ Iām looking for help with ...
- š¬ Ask me about ...
- š« How to reach me: ...
- š Pronouns: ...
- ā” Fun fact: ...
-->
# Original code from https://github.com/pybind/cmake_example/blob/master/setup.py

import os
import re
import sys
import platform
import subprocess
import multiprocessing

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(
                re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.8.2':
                raise RuntimeError("CMake >= 3.8.2 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(
            self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable,
                      '-DBUILD_FROM_PIP=ON']

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        env = os.environ.copy()

        if platform.system() == "Windows":
            cmake_args += [
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            num_jobs = env.get('NUM_JOBS', multiprocessing.cpu_count())
            build_args += ['--', '-j%s' % str(num_jobs), 'pyBaba']

        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] +
                              cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] +
                              build_args, cwd=self.build_temp)
\033[1;92m _____     _     _
|  ___|_ _(_)___(_)
\033[1;96m| |_ / _` | |_  / |
|  _| (_| | |/ /| |
\033[1;97m|_|  \__,_|_/___|_|
\033[1;37m--------------------------------------------------
\033[1;96mā£ OWNER  (š) Faizi
\033[1;94mā£ WHATSAPP  (š„)03117826879
\033[1;37m--------------------------------------------------
"""

setup(
    name='pyfaizi',
    version='0.1',
    author='Chris Ohk',
    author_email='cazhar529@gmail.com',
    description='faizi Is You simulator with some reinforcement learning',
    long_description='',
    ext_modules=[CMakeExtension('pyfaizi')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
