from distutils.core import setup

VERSION = '0.1'
DESCRIPTION = 'YT video stream downloader'
LONG_DESCRIPTION = 'Package for aquiring binary data for YouTube videos with age restrictions.'

# Setting up
setup(
    name='YT_vid_DL',
    packages=['YT_vid_DL'],
    version=VERSION,
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    author="Moonbox88 (Sean Mooney)",
    author_email="<seanmooney@live.co.uk>",
    url='https://github.com/Moonbox88/YT_Downloader.git',
    download_url='https://github.com/Moonbox88/YT_vid_DL/archive/refs/tags/v0.1.tar.gz',
    install_requires=['pytube', 'ffmpy'],
    keywords=['python', 'video', 'stream', 'YouTube'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
