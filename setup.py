from setuptools import setup, find_packages


setup(
    name='text_to_condition',
    version='0.0.1',
    author='Yaron Gonen',
    author_email='yaron.gonen@gmail.com',
    description='A module to convert text to formal condition using LLM',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yarongon/text_to_condition',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=open('requirements.txt').read().splitlines(),
)
