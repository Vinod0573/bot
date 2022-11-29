from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = "1.1.0"

long_description = "Long Description"

tests_requires = []


install_requires = [
    'certifi==2019.6.16',
    'chardet==3.0.4',
    'Click==7.0',
    'coloredlogs==10.0',
    'ConfigArgParse==0.14.0',
    'Flask==1.1.1',
    'Flask-Cors==3.0.8',
    'future==0.17.1',
    'gevent==1.4.0',
    'greenlet==0.4.15',
    'humanfriendly==4.18',
    'idna==2.8',
    'itsdangerous==1.1.0',
    'Jinja2==2.10.1',
    'MarkupSafe==1.1.1',
    'monotonic==1.5',
    'rasa-sdk==1.1.0',
    'requests==2.22.0',
    'six==1.12.0',
    'typing==3.7.4',
    'urllib3==1.25.3',
    'Werkzeug==0.15.5'
]

extras_requires = {
    "test": tests_requires
}

setup(
    name="rasa_sdk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(exclude=["tests", "tools"]),
    version=__version__,
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require=extras_requires,
    include_package_data=True,
    description="Machine learning based dialogue engine "
                "for conversational software.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Saarthi',
    author_email='hi@saarthi.com',
    maintainer="Snehasish Mishra",
    maintainer_email="snehasish@saarthi.com",
    license="Free",
    keywords="nlp machine-learning machine-learning-library bot bots "
             "botkit rasa conversational-agents conversational-ai chatbot"
             "chatbot-framework bot-framework",
    url="https://saarthi.com",
    download_url= "",
    project_urls={
        "Bug Reports": "https://saarthi.com",
        "Documentation": "https://saarthi.com",
        "Source": "https://saarthi.com",
    },
)

print("\nWelcome to Rasa SDK for version 1.0!")
