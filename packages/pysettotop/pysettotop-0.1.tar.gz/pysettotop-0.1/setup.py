import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pysettotop",
    version = "0.1",
    author = "Swordysrepo",
    author_email = "swordysrepo@gmail.com",
    description = ("used for selecting a window and bringing it to the top of other applications."),
    license = "MIT",
    keywords = "python windows top win32 settotop",
    url = "https://github.com/swordysrepo/settotop",
    download_url = 'https://github.com/swordysrepo/settotop.git',
    packages=['settotop'],
    entry_points = {
        "console_scripts": ['settotop = settotop.settotop:main']
        },
    long_description=read('README.md'),
    install_requires=[
          'pywin32'
      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'Operating System :: Microsoft',
        'Environment :: Win32 (MS Windows)',
    ],
)
