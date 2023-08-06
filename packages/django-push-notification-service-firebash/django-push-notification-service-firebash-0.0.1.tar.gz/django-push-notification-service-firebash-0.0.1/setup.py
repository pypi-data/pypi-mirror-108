import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(BASE_DIR, 'kjdskjskjkj')

setuptools.setup(
    name="django-push-notification-service-firebash",
    version="0.0.1",
    author="Ritesh Bajpai",
    author_email="bajpairitesh878@gmail.com",
    description="Use for Firebash Phone Push Notification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/bajpairitesh878/django_firebash_push_service",
    project_urls={
        "Bug Tracker": "https://gitlab.com/bajpairitesh878/django_firebash_push_service/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={BASE_DIR: "dj_push"},
    packages=setuptools.find_packages(where=BASE_DIR),
    python_requires=">=3.6",
)