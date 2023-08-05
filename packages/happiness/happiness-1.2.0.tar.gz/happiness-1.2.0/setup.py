from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='happiness',
      version='1.2.0',
      description='this package is for spreading happiness',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Devansh Gupta',
      author_email='xyznfc@gmail.com',
      license='MIT',
      packages=['happiness'],
      install_requires=[
          'life',
      ],
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ]
)

