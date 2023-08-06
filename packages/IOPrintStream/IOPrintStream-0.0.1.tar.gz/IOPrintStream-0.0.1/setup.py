from setuptools import setup

def readme():
    with open('README.md') as f:
        f.read()

setup(
   name='IOPrintStream',
   version='0.0.1',
   description='A useful module',
   long_description = readme(),
   long_description_content_type='text/markdown',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['IOPrintStream'],  #same as name
   install_requires=[], #external packages as dependencies
)