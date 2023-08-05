from setuptools import setup,find_packages


setup(
   name='devlist',
   version='0.1',
   description='DevList API in a simple python package',
   license="MIT",
   long_description=open('README.txt').read(),
   author='Zaid Ali',
   author_email='realarty69@gmail.com',
   keywords=['api'],
    packages=['devlist'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)