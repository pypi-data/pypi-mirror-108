CARNA_PY_VERSION = '0.0.7'

# Build and install:
# > python setup.py bdist_wheel
# > python -m pip install --force-reinstall CarnaPy/dist/*.whl
# 
# Distribute to PyPI:
# > python setup.py sdist
# > python -m twine upload dist/*.tar.gz

import sys
import os

from pathlib import Path

root_dir = Path(os.path.abspath(os.path.dirname(__file__)))

def build(dry, call):
    build_dir_debug   = root_dir / 'cbuild' / 'make_debug'
    build_dir_release = root_dir / 'cbuild' / 'make_release'

    get_cmake_args = lambda debug: [
        f'-DCMAKE_BUILD_TYPE={"Debug" if debug else "Release"}',
        f'-DBUILD_TEST=ON',
        f'-DBUILD_DOC={"OFF" if debug else "ON"}',
        f'../..',
    ]

    import packaging.version
    if not dry:

        version = packaging.version.parse(CARNA_PY_VERSION)
        with open(root_dir / 'version.cmake', 'w') as io:
            io.write(f'set(MAJOR_VERSION {version.major})\n')
            io.write(f'set(MINOR_VERSION {version.minor})\n')
            io.write(f'set(PATCH_VERSION {version.micro})\n')

        build_dir_debug  .mkdir(parents=True, exist_ok=True)
        build_dir_release.mkdir(parents=True, exist_ok=True)

        os.chdir(str(build_dir_debug))
        call(['cmake'] + get_cmake_args(debug=True))
        call(['make', 'VERBOSE=1'])
        call(['make', 'RUN_TESTSUITE'])

        os.chdir(str(build_dir_release))
        call(['cmake'] + get_cmake_args(debug=False))
        call(['make', 'VERBOSE=1'])
        call(['make', 'RUN_TESTSUITE'])

    os.chdir(str(root_dir))

if len(sys.argv) > 1 and sys.argv[1] == '--build-only':

    import subprocess
    build(False, subprocess.call)
    
else:

    from setuptools import setup, Extension, find_packages
    from setuptools.command.build_ext import build_ext as build_ext_orig

    with open(root_dir / 'README.md', encoding='utf-8') as io:
        long_description = io.read()

    class CMakeExtension(Extension):

        def __init__(self):
            super().__init__('CMake', sources=[])


    class build_ext(build_ext_orig):

        def run(self):
            for ext in self.extensions:
                self.build_cmake(ext)
            super().run()

        def build_cmake(self, ext):
            build(self.dry_run, self.spawn);


    setup(
        name = 'CarnaPy',
        version = CARNA_PY_VERSION,
        description = 'General-purpose real-time 3D visualization',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        author = 'Leonid Kostrykin',
        author_email = 'leonid.kostrykin@bioquant.uni-heidelberg.de',
        url = 'http://evoid.de',
        include_package_data = True,
        license = 'MIT',
        package_dir = {
            'carna': 'cbuild/make_release/carna',
            'carna_debug': 'cbuild/make_debug/carna',
        },
        packages = ['carna', 'carna_debug'],
        package_data = {
            'carna': ['*.so'],
            'carna_debug': ['*.so'],
        },
        ext_modules = [CMakeExtension()],
        cmdclass={
            'build_ext': build_ext,
        },
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Environment :: GPU',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: C++',
            'Programming Language :: Python',
            'Topic :: Education',
            'Topic :: Multimedia :: Graphics :: 3D Rendering',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Software Development :: User Interfaces',
        ],
        setup_requires = [
            'packaging',
        ],
        install_requires = [
            'numpy',
        ],
    )

