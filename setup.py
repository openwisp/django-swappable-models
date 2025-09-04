from setuptools import setup

LONG_DESCRIPTION = """
The unofficial Django swappable models API.
"""


def readme():
    try:
        with open("README.md", encoding="utf-8") as f:
            return f.read()
    except IOError:
        return LONG_DESCRIPTION


setup(
    name="swapper",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="S. Andrew Sheppard",
    author_email="andrew@wq.io",
    url="https://github.com/openwisp/django-swappable-models",
    license="MIT",
    packages=["swapper"],
    description=LONG_DESCRIPTION.strip(),
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
    ],
    tests_require=["django>=4.2"],
    python_requires=">=3.9",
)
