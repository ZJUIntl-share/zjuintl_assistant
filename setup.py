from setuptools import setup

setup(
    name='zjuintl_assistant',
    version='0.0.1',
    description='Python interface for getting data from different platforms of ZJU International College',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ZJUIntl-share/zjuintl_assistant',
    author='ZJUIntl-share',
    license='MIT',
    packages=['zjuintl_assistant'],
    install_requires=[
        'rsa',
        'requests',
        'beautifulsoup4',
    ],
    python_requires='>=3',
    zip_safe=False
)