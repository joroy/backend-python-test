from setuptools import find_packages, setup

setup(
    name='alayatodo',
    version='1.0.0',
    url='https://github.com/joroy/backend-python-test',
    license='BSD',
    maintainer='Me',
    maintainer_email='me@somewhere.com',
    description='Alayacare backend-python-test-joroy',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
