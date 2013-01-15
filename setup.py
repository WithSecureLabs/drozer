import fnmatch
import glob
import os
import setuptools

def find_libs(src):
    matches = []
    
    for root, dirnames, filenames in os.walk(src):
        for filename in fnmatch.filter(dirnames, 'libs'):
            matches.extend(glob.glob(os.path.join(root, filename, "*", "*")))

    return matches
    
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
  package_data = { "": ["*.apk", "*.bks", "*.crt", "*.jar", "*.key", "*.sh", "busybox"] + find_libs("src") },
  scripts = ["bin/mercury", "bin/mercury-console", "bin/mercury-server", "bin/mercury-ssl"],
  install_requires = ["protobuf==2.4.1", "pyopenssl"],
  classifiers = [])
