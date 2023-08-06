__version__ = '1.0.0'

from setuptools import setup

setup(
    name="calapi",
    version=__version__,
    description="A light weight python wrapper for Google's Calendar API v3 written upon Google API Python Client.",
    long_description="""Google calendar python api wrapper for Google's Calendar Reporting API v3 using Googles API python client.""",
    long_description_content_type="text/plain",
    author="Rakesh Gunduka",
    packages=["calapi"],
    package_data={},
    author_email="rakesh.gunduka@gmail.com",
    url="http://github.com/rakeshgunduka/calapi/",
    install_requires=[
        "google-api-python-client==2.5.0",
        "google-api-core==1.28.0",
        "google-auth==1.30.0",
        "google-auth-oauthlib==0.4.4",
        "google-auth-httplib2==0.1.0"
    ],
    license="http://www.opensource.org/licenses/mit-license.php",
    keywords="google calendar api client",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
