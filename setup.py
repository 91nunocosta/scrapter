from setuptools import setup

setup(name='scrapter',
      version='0.1.0',
      description='Extension to Scrapy for update databases.',
      url='https://github.com/91nunocosta/scrapter',
      author='Nuno Costa',
      author_email='91nunocosta@gmail.com',
      license='MIT',
      packages=['scrapter'],
      zip_safe=False,
      install_requires=[
          'pymongo',
          'scrapy',
          'mongomock'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['scrapter=scrapter.run:execute']
      })
