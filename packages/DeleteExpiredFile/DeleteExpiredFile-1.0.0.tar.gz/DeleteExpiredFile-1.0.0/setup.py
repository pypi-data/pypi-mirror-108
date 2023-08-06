# coding:utf-8

from setuptools import setup
# or
# from distutils.core import setup  
foruser = '''# Author:KuoYuan Li '''
setup(
        name='DeleteExpiredFile',   
        version='1.0.0',   
        description='delete expired file with function or thread',
        long_description=foruser,
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/DeleteExpiredFile',      
        packages=['DeleteExpiredFile'],   
        include_package_data=True,
        keywords = ['delete files', 'delete expired files','delete rountine'],   # Keywords that define your package best
        #install_requires=['threading'],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
      ],
)
