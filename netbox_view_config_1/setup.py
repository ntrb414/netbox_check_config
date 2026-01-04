from setuptools import setup, find_packages

setup(
    name='netbox-view-config',
    version='0.1',
    description='A NetBox plugin to view device configuration via SSH',
    install_requires=[
        'netmiko',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
