import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(name="polly_repositories",
      version="0.0.1",
      description="Interact with Polly Repositories",
      long_description=README,
      long_description_content_type="text/markdown",
      author="Bisweswar Martha",
      author_email="bisweswar.martha@elucidata.io",
      packages=find_packages(),
      include_package_data=True)
