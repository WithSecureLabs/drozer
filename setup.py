import fnmatch
import glob
import os
import setuptools
import re
import subprocess

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

def clear_apks():
	for root, dirnames, filenames in os.walk('src/drozer/modules'):
		for filename in filenames:
			if (fnmatch.fnmatch(filename, "*.class") or fnmatch.fnmatch(filename, "*.apk")):
				#print os.path.join(root, filename)
				os.remove(os.path.join(root, filename))

def make_apks():

	lib = os.path.dirname(os.path.realpath(__file__))+'/src/drozer/lib/'

	#If apks exist, delete them and regenerate
	clear_apks()

	# Generate apks
	for root, dirnames, filenames in os.walk('src/drozer/modules'):
		for filename in filenames:
			if (fnmatch.fnmatch(filename, "*.java")):
				#Compile java
				subprocess.call(['javac -cp '+ lib+'android.jar '+filename],shell=True,cwd=root)
				
				#Build apk
				m = re.search('(.+?)(\.[^.]*$|$)',filename)
				subprocess.call([lib+'dx --dex --output='+m.group(1)+'.apk '+m.group(1)+'*.class'],shell=True,cwd=root)

def get_package_data():
	data = {"":[]}

	#Make sure we build apks before generating a package
	make_apks()

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