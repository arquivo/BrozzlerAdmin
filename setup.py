from setuptools import setuptools, find_packages

setuptools.setup(
    name='Brozzler Admin',
    version='0.5.4',
    packages=find_packages(),
    package_data={'': ['static/**/*','templates/*','job_templates/*','*.yaml']},
    include_package_data=True,
    license='Apache License 2.0',
    long_description=open('README.md').read(),
    author_email='daniel.bicho@fccn.pt',
    url='https://github.com/arquivo/BrozzlerAdmin',
    entry_points={
        'console_scripts': [
            'bc-get-outlinks=brozzleradmin.cli:get_all_outlinks',
            'bc-resume-job=brozzleradmin.cli:resume_job',
            'bc-get-job-queue=brozzleradmin.cli:get_job_queue',
            'bc-launch-ui=brozzleradmin.app:main'
        ]
    },
    install_requires=[
        'Flask==1.1.1',
        'flask-wtf==0.14.3',
        'apscheduler',
        'brozzler>=1.5.7',
        'WTForms==2.2.1',
        'rethinkdb>=2.3,<2.4',
        'doublethink>=0.2.0',
        'PyYAML',
        'Jinja2==2.11.3'
    ]
)
