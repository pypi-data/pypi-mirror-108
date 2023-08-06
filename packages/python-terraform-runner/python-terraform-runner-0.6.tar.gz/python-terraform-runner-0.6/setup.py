from distutils.core import setup

DEPENDENCIES = [
    'python_terraform',
    'requests',
    'argparse'
]

VERSION = '0.6'
URL = 'https://github.com/deknijf/python-terraform-runner'

setup(
    name='python-terraform-runner',
    #packages=['tf-runner'],
    version=VERSION,
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='Apache Software License',
    # Give a short description about your library
    description='Script to run terraform in gitlab CI and post notifications to slack (via a webhook)',
    author='Bert De Knijf',
    author_email='bert.deknijf@gmail.com',
    # Provide either the link to your github or to your website
    url=URL,
    # Keywords that define your package best
    keywords=['python', 'terraform', 'slack', 'gitlab'],
    install_requires=DEPENDENCIES,
    scripts=['bin/terraform-gitlab'],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
)
