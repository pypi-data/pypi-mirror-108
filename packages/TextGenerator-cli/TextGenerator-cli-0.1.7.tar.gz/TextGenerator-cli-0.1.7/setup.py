from setuptools import find_packages, setup

from TextGenerator import __version__

setup(
    name='TextGenerator-cli',
    version=__version__,
    description='マルコフ連鎖を使った文章自動生成プログラム+CLI',
    description_content_type='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eggplants/TextGenerator-cli',
    author='eggplants',
    packages=find_packages(),
    python_requires='>=3.5',
    include_package_data=True,
    license='MIT',
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'textgen=TextGenerator.main:main'
        ]
    }
)
