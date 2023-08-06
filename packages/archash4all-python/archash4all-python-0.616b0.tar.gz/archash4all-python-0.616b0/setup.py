from setuptools import setup, Extension, find_packages
import platform

_os = platform.system()

if _os == "Linux":
    compile_args = ['-Wall',
                    '-Wno-unused-but-set-variable',
                    '-Wno-unused-variable',
                    '-Wno-pointer-sign',
                    '-Wno-endif-labels']
elif _os == "Windows":
    compile_args = ['/wd4101', '/wd4267']
else:
    compile_args = []

setup(
    name="archash4all-python",
    version="0.616-beta",
    author="J.R w/ TheSnowfield",
    description="Generate x-random-challenge for arcapi requests",
    license="MIT License",
    platforms="any",
    keywords=["Python", "hashing"],
    python_requires='>=3.1',
    ext_modules=[Extension(
        'archash4all', [
            'archash4all/c-module/b64.c/buffer.c',
            'archash4all/c-module/b64.c/decode.c',
            'archash4all/c-module/b64.c/encode.c',
            'archash4all/c-module/bmw.c',
            'archash4all/c-module/archash.c',
        ], extra_compile_args=compile_args
    )],
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"])
)
