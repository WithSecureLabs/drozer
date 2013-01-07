import os
import setuptools

setuptools.setup(
  name = "mercury",
  version = "2.1.0",
  author = "MWR InfoSecurity",
  author_email = "mercury@mwrinfosecurity.com",
  description = "The Heavy Metal that Poisoned the Droid.",
  long_description = open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
  license = "MWR Code License v2",
  keywords = "android security framework",
  url = "http://mwr.to/mercury",

  packages = setuptools.find_packages("src"),
  package_dir = { "": "src" },
  package_data = { "": ["*.apk", "busybox"] },
  scripts = ["bin/mercury", "bin/mercury-console", "bin/mercury-server"],
  install_requires = ["protobuf==2.4.1"],
  classifiers = [])
