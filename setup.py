"""
setup for ddnsbroker
"""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ddnsbroker',
    version='0.1',
    description='A broker for the dynamic dns updates',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jomority/ddnsbroker',
    author='Moritz Jordan',
    author_email='jomority@openotter.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: Name Service (DNS)',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    keywords='dyndns ddns dynamic dns django dyndns2',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=[
        'django>=3.0',
        'requests',
    ],
    project_urls={  # Optional
        'Source': 'https://github.com/jomority/ddnsbroker',
        'Bug Reports': 'https://github.com/jomority/ddnsbroker/issues',
    },
    include_package_data=True,
    zip_safe=True,
)
