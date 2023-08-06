from distutils.core import setup

setup(name= 'mrxxwnester',
      version= '1.0.0',
      py_modules=['mrxxwnester'],
      author ='xxw',
      url= 'http://www.headfirstlabs.com',
      description='A simple printer of nested lists',
      package_dir={'mrxxw': 'mrxxw'},
      package_data={'mrxxw': ['*.*', 'mrxxw/*']},
      )