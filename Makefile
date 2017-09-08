
NATIVES = $(shell find src/drozer/modules -name Android.mk)
SOURCES = $(shell find src/drozer/modules -name *.java)

DX = $(CURDIR)/src/drozer/lib/dx
JAVAC = javac
NDKBUILD = ndk-build
PYTHON = python
CP=cp
SED=sed
CD=cd
MD5=md5sum
FIND=find
GREP=grep
VERSION=`git describe --tags  | cut -c 1-5`
TAR=tar


SDK = $(CURDIR)/src/drozer/lib/android.jar

all: sources deb rpm
	@echo
	@echo "----------------------------------------"
	@echo
	@echo "drozer"
	@echo "You are almost ready to run drozer..."
	@echo
	@echo "To finish preparing your environment run:"
	@echo
	@echo "  $$ source ENVIRONMENT"
	@echo
	@echo "Then you should be able to run 'drozer' to see the available commands."
	@echo
	@echo "----------------------------------------"
	@echo
apks: $(SOURCES:.java=.apk)
clean:
	find -name *.pyc |xargs rm -f
	rm -f $(SOURCES:.java=.class) $(SOURCES:.java=.apk)
native-libraries: $(NATIVES)
sources: src/pydiesel/api/protobuf_pb2.py
test: force
	$(PYTHON) test/mwr_test/all.py

%.apk: %.class
	cd $(dir $^); $(DX) --dex --output=$(notdir $(^:.class=.apk) $(^:.class=*.class))
%.class: %.java
	cd $(dir $^); $(JAVAC) -cp $(SDK) $(notdir $^)
%.mk: force
	cd $(dir $@); $(NDKBUILD)

common/protobuf.proto:
	git submodule init && git submodule update
src/pydiesel/api/protobuf_pb2.py: common/protobuf.proto
	cd common; protoc --python_out=../src/pydiesel/api/ protobuf.proto

drozer-prepared: src/pydiesel/api/protobuf_pb2.py apks
	mkdir -p dist

deb: drozer-deb-structure debian/DEBIAN/control debian/DEBIAN/md5sums
	dpkg -b debian
	mv debian.deb dist/drozer_${VERSION}.deb

drozer-deb-structure: drozer-prepared
	mkdir -p debian/etc/bash_completion.d
	mkdir -p debian/usr/bin
	mkdir -p debian/usr/lib/python2.7/dist-packages
	mkdir -p debian/usr/share/doc/drozer
	mkdir -p debian/DEBIAN
	# copy drozer components into the debian archive
	$(CP) scripts/drozer debian/etc/bash_completion.d/drozer
	$(CP) bin/* debian/usr/bin/
	$(CP) LICENSE debian/usr/share/doc/drozer/LICENSE
	$(CP) README.md debian/usr/share/doc/drozer/README.md
	$(CP) -r src/drozer debian/usr/lib/python2.7/dist-packages/drozer
	$(CP) -r src/mwr debian/usr/lib/python2.7/dist-packages/mwr
	$(CP) -r src/pydiesel debian/usr/lib/python2.7/dist-packages/pydiesel

debian/DEBIAN/control: 
	$(CP) scripts/deb/control.template debian/DEBIAN/control
	$(CP) scripts/deb/postinst debian/DEBIAN/postinst
	$(CP) scripts/deb/prerm debian/DEBIAN/prerm
	# overwrite the Installed-size: field with the correct size
	$(SED) -i s/\<FILE_SIZE\>/${shell du -s debian --exclude=DEBIAN debian |cut -f 1}/g debian/DEBIAN/control
	$(SED) -i s/\<VERSION\>/${VERSION}/g debian/DEBIAN/control
	
debian/DEBIAN/md5sums:
	$(CD) debian && $(MD5) `$(FIND) . -type f |$(GREP) -v '^[.]/DEBIAN/'` > DEBIAN/md5sums

rpm: drozer-rpm-structure
	$(CD) redhat && rpmbuild --define "_topdir `pwd`" -bb SPECS/drozer.spec
	mv redhat/RPMS/noarch/*.rpm ./dist/

drozer-rpm-structure: drozer-prepared
	mkdir -p dist
	mkdir -p redhat/SPECS
	mkdir -p redhat/SOURCES/drozer-${VERSION}
	mkdir -p redhat/SOURCES/drozer-${VERSION}/etc/bash_completion.d
	mkdir -p redhat/SOURCES/drozer-${VERSION}/usr/bin
	mkdir -p redhat/SOURCES/drozer-${VERSION}/usr/share/applications
	mkdir -p redhat/SOURCES/drozer-${VERSION}/usr/share/doc/drozer
	mkdir -p redhat/SOURCES/drozer-${VERSION}/usr/lib/python2.7/dist-packages
	# copy drozer components into the rehat archive
	touch redhat/SOURCES/drozer-${VERSION}/configure
	$(CP) scripts/drozer redhat/SOURCES/drozer-${VERSION}/etc/bash_completion.d/drozer
	$(CP) bin/* redhat/SOURCES/drozer-${VERSION}/usr/bin
	$(CP) LICENSE redhat/SOURCES/drozer-${VERSION}/usr/share/doc/drozer/LICENSE
	$(CP) README.md redhat/SOURCES/drozer-${VERSION}/usr/share/doc/drozer/README.md
	$(CP) -r src/drozer redhat/SOURCES/drozer-${VERSION}/usr/lib/python2.7/dist-packages/drozer
	$(CP) -r src/mwr redhat/SOURCES/drozer-${VERSION}/usr/lib/python2.7/dist-packages/mwr
	$(CP) -r src/pydiesel redhat/SOURCES/drozer-${VERSION}/usr/lib/python2.7/dist-packages/pydiesel
	# compress the structure into a tarball
	$(TAR) czvf redhat/SOURCES/drozer-${VERSION}.tar.gz -C redhat/SOURCES drozer-${VERSION}
	rm -rf redhat/SOURCES/drozer-${VERSION}
	# Copy spec file to 
	$(CP) scripts/rpm/drozer.spec redhat/SPECS/

force: ;
