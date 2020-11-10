from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='importlinter',
      version='0.1',
      description='Check and fix your module and package imports in python files',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/JakeRoggenbuck/ImportLinter',
      author='Jake Roggenbuck',
      author_email='jake@jr0.org',
      license='MIT',
      py_modules=['importlinter'],
      zip_safe=False,
      entry_points={
            'console_scripts': [
                'importlinter = importlinter:run'
            ]
      },
)
