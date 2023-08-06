from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
]

setup(
    name='hyaline',
    version='0.0.1',
    description='Discord API Wrapper for Python! (Not Finished.)',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/5elenay/hyaline/',
    author='5elenay',
    author_email='',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/5elenay/hyaline/issues",
    },
    classifiers=classifiers,
    keywords=["discord", "wrapper", "api", "gateway", "lightweight", "discord-api"],
    packages=find_packages(),
    install_requires=['python-dateutil', 'aiohttp']
)
