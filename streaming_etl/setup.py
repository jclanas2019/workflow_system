from setuptools import setup, find_packages

setup(
    name='streaming_etl_project',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'run_etl=scripts.run_etl:main',
            'run_secure_server=scripts.run_secure_server:main',
            'run_secure_client=scripts.run_secure_client:main'
        ]
    }
)
