from setuptools import setup, find_packages

import fluid_report

setup(
    name="fluid_report",
    version=fluid_report.__version__,
    packages=find_packages(),
    install_requires=[
        'fluid_mq>=3.0.0rc2',
        'splunk-sdk==1.6.0',
        'iso8601==0.1.10',
        'six==1.10.0',
        'requests-toolbelt==0.6.0',
    ],
    author="A-Team Developers",
    author_email="atd@lodgenet.com",
    url="http://pypi.lodgenet.com/simple/fluid_report",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'reportbot = fluid_report.reportbot:main',
        ],
    },
)
