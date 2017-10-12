import setuptools

setuptools.setup(
    name='BrozzlerController',
    version='0.1dev',
    packages=['brozzleradmin'],
    license='Apache License 2.0',
    long_description=open('README.md').read(),
    author_email='daniel.bicho@fccn.pt',
    url='',
    entry_points={
        'console_scripts': [
            'bc-get-outlinks=brozzleradmin.cli:get_all_outlinks',
            'bc-resume-job=brozzleradmin.cli:resume_job'
        ]
    }
)
