from setuptools import setup, find_packages

setup(
    name='tablebase',
    version='1.5.3',
    description='A lightweight tool to make tables easily in python.',
    long_description="For documentation go to \n https://dev.centillionware.com/tablebase",
    author='Maximilian Lange',
    author_email='maxhlange@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
