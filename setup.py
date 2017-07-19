import fnmatch
import glob
import os
import setuptools
import re

from src.drozer import meta
from sys import platform

def find_files(src):
    matches = []

    for root, dirnames, filenames in os.walk(src):
        matches.extend(map(lambda f: os.path.join(root, f), filenames))

    return matches

def find_libs(src):
    matches = []

    for root, dirnames, filenames in os.walk(src):
        for filename in fnmatch.filter(dirnames, 'lib'):
            matches.extend(glob.glob(os.path.join(root, filename, "*", "*")))
        for filename in fnmatch.filter(dirnames, 'libs'):
            matches.extend(glob.glob(os.path.join(root, filename, "*", "*")))

    return map(lambda fn: os.path.basename(fn), filter(lambda fn: os.path.isfile(fn), matches))

# Do a system check when installing bash complete script
def get_install_data():
	install_data = []
	if platform == "linux" or platform == "linux2":
		install_data = [('/etc/bash_completion.d',['scripts/drozer'])]

	return install_data

def get_executable_scripts():
  scripts = ["bin/drozer", "bin/drozer-complete", "bin/drozer-repository"]
  if platform == "win32":
    scripts.append("bin/drozer.bat")

  return scripts

def get_package_data():
	data = {"":[]}

	for root, dirnames, filenames in os.walk('src/drozer'):
		for filename in filenames:
			if not (fnmatch.fnmatch(filename, "*.class") or fnmatch.fnmatch(filename, "*.pyc")):
				m = re.search('src\/drozer\/(.*)', os.path.join(root, filename))
				if m:
					data[""].append(m.group(1))
	return data

setuptools.setup(
  name = meta.name,
  version = str(meta.version),
  author = meta.vendor,
  author_email = meta.contact,
  description = meta.description,
  long_description = meta.long_description,
  license = meta.license,
  keywords = meta.keywords,
  url = meta.url,

  packages = setuptools.find_packages("src"),
  package_dir = {   "drozer": "src/drozer",
                    "mwr": "src/mwr",
                    "pydiesel": "src/pydiesel" },
  package_data = get_package_data(),
  scripts = get_executable_scripts(),
  install_requires = ["protobuf>=2.6.1","pyopenssl>=16.2", "pyyaml>=3.11"],
  data_files = get_install_data(),
  classifiers = [])