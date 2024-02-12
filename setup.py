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

def get_pwd():
	pwd = ''

	if platform == "linux" or platform == "linux2" or platform == "darwin":
		pwd = 'src/drozer'
	elif platform == "win32":
		pwd = 'src\\drozer'

	return pwd

def clear_apks():
	pwd = get_pwd()

	if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
		pwd += '/modules'
	elif platform == 'win32':
		pwd += '\\modules'

	for root, dirnames, filenames in os.walk(pwd):
		for filename in filenames:
			if (fnmatch.fnmatch(filename, "*.class") or fnmatch.fnmatch(filename, "*.apk") or fnmatch.fnmatch(filename, "*.zip")):
				#print os.path.join(root, filename)
				os.remove(os.path.join(root, filename))

def make_apks():

	pwd = get_pwd()
	lib = os.path.dirname(os.path.realpath(__file__))
	d8 =''

	if platform == 'linux' or 'linux2' or 'darwin':
		pwd += '/modules'
		lib += '/src/drozer/lib/'
		d8 = 'd8'
	elif platform == 'win32':
		pwd += '\\modules'
		lib += '\\src\\drozer\\lib\\'
		d8 = 'd8.bat'

	#If apks exist, delete them and generate new ones
	clear_apks()

	# Generate apks

	for root, dirnames, filenames in os.walk(pwd):
		for filename in filenames:
			if (fnmatch.fnmatch(filename, "*.java")):
				#Compile java
				javac_cmd = ['javac', '-cp', lib+'android.jar', filename]

				#Build apk
				m = re.search('(.+?)(\.[^.]*$|$)',filename)
				d8_cmd = [lib+d8, '--output', m.group(1)+'.zip', m.group(1)+'*.class', '--lib', lib+'android.jar']

				if platform == "linux2" or platform == "linux" or platform == "darwin":
					subprocess.call(' '.join(javac_cmd),shell=True,cwd=root)

					subprocess.call(' '.join(d8_cmd),shell=True,cwd=root)

					subprocess.call(' '.join(['mv', m.group(1)+'.zip', m.group(1)+'.apk']),shell=True,cwd=root)
				elif platform == "win32":
					subprocess.call(javac_cmd,shell=True,cwd=root)

					subprocess.call(d8_cmd,shell=True,cwd=root)

					subprocess.call(' '.join(['move', m.group(1)+'.zip', m.group(1)+'.apk']),shell=True,cwd=root)

def get_package_data():
	data = {"":[]}
	pwd = get_pwd()

	#Make sure we build apks before generating a package
	# DEBUG DISABLE
	#make_apks()

	for root, dirnames, filenames in os.walk(pwd):
		for filename in filenames:
			if not (fnmatch.fnmatch(filename, "*.class") or fnmatch.fnmatch(filename, "*.pyc")):
				data[""].append(os.path.join(root, filename)[11:])
	return data

setuptools.setup(
  name = meta.name,
  version = meta.version,
  author = meta.vendor,
  author_email = meta.contact,
  description = meta.description,
  long_description = meta.long_description,
  license = meta.license,
  keywords = meta.keywords,
  url = meta.url,

  packages = setuptools.find_packages("src"),
  package_dir = {   "drozer": "src/drozer",
                    "WithSecure": "src/WithSecure",
                    "pysolar": "src/pysolar" },
  package_data = get_package_data(),
  scripts = get_executable_scripts(),
  install_requires = ["protobuf>=2.6.1","pyopenssl>=16.2", "pyyaml>=3.11"],
  data_files = get_install_data(),
  classifiers = [])
