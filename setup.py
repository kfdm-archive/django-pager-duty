try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-pager-duty',
    description='PagerDuty Filtering and On Call Display',
    author='Paul Traylor',
    url='http://github.com/kfdm/django-pager-duty/',
    version='0.2.1',
    packages=['pagerduty'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
