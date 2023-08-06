from setuptools import setup, find_packages


setup(
    name='example_publish_pypi_medium',
    version='0.3',
    license='MIT',
    author="Giorgos Myrianthous",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'example_publish_pypi_medium': 'example_publish_pypi_medium'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)
