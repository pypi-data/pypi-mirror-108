import setuptools
import print_dir

with open('Readme.md') as fr:
    long_description = fr.read()

setuptools.setup(
    name='pr_dir',
    version=print_dir.__version__,
    author='Tarasenko V.E.',
    author_email='gidekoj@mail.ru',
    description='Directory`s files console-visualizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gideko1/print_dir',
    packages=setuptools.find_packages(),
    install_requires=[],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)
