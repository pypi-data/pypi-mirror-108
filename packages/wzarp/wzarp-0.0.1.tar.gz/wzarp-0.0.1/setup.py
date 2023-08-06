import setuptools
import wzarp

with open('readme.md') as fr:
    long_description = fr.read()

setuptools.setup(
    name='wzarp',
    version=wzarp.__version__,
    author='Marunov V.A.',
    author_email='marunov02@mail.ru',
    description='Wzarp is a Weather library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Falangizzle/wzarp',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup>=4.9.3'
    ],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"],
)