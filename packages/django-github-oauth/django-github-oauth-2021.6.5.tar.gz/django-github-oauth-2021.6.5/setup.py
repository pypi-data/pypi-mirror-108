from setuptools import setup

setup(
    name='django-github-oauth',
    version='2021.6.5',
    install_requires=[
        'requests'
    ],
    packages=[
        'django_github_oauth',
        'django_github_oauth.urls'
    ]
)
