from setuptools import setup

def readme():
    with open('README.md') as f:
        f.read()

setup(
   name='IOConsole',
   version='0.0.1',
   description='A useful module',
   long_description = readme(),
   long_description_content_type='text/markdown',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['IOConsole'],  #same as name
   install_requires=['IOPrintStream'], #external packages as dependencies
)