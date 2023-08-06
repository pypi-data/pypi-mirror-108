from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='telegram_simulation_bot',
    version='v0.1',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/AaronDavidSchneider/telegram_simulation_bot',
    license='MIT',
    author='Aaron David Schneider',
    author_email='aarondavid.schneider@nbi.ku.dk',
    description='Interact with your computing cluster via telegram to get realtime information on your running jobs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['bin/telegram_simulation_bot'],
    install_requires=[
        "f90nml>=1.3.1",
        "telethon",
        "appdirs",
        "pyyaml",
    ]
)
