import fnmatch
import glob
import os
import setuptools

from drozer import meta

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
    
setuptools.setup(
  name = meta.name,
  version = str(meta.version),
  author = meta.vendor,
  author_email = meta.contact,
  description = meta.description,
  long_description = open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
  license = meta.license,
  keywords = meta.keywords,
  url = meta.url,

  packages = setuptools.find_packages("src"),
  package_dir = {   "drozer": "src/drozer",
                    "mwr": "src/mwr",
                    "pydiesel": "src/pydiesel" },
  package_data = { "": ["*.apk", "*.bks", "*.crt", "*.docx", "*.jar", "*.key", "*.sh", "*.xml", "busybox"] + find_libs("src"),
                   "drozer": ["lib/aapt",
                              "lib/aapt.exe",
                              "lib/*.apk",
                              "lib/*.jar",
                              "lib/*.pem",
                              "lib/*.pk8",
                              "lib/weasel/armeabi/w",
                              "server/web_root/*" ] },
  scripts = ["bin/drozer", "bin/drozer-complete"],
  install_requires = ["protobuf==2.4.1", "pyopenssl==0.13"],
  classifiers = [])
