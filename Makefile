
NATIVES = $(shell find src/drozer/modules -name Android.mk)
SOURCES = $(shell find src/drozer/modules -name *.java)

DX = dx
JAVAC = javac
NDKBUILD = ndk-build
PYTHON = python

SDK = $(CURDIR)/src/drozer/lib/android.jar

all: dist-egg dist-windows
apks: $(SOURCES:.java=.apk)
clean:
	find -name *.pyc |xargs rm -f
	rm -f $(SOURCES:.java=.class) $(SOURCES:.java=.apk)
	rm -rf build/* dist/*
dist-egg: sources apks native-libraries
	$(PYTHON) setup.py bdist_egg
dist-windows: sources apks native-libraries
	$(PYTHON) setup.py bdist_wininst
lint: force
	cd src && pylint . -d C0103,C0301,E1101,R0201,R0902,R0903,R0904,R0911,R0913,W0108,W0141,W0142,W0631 --ignore protobuf_pb2.py,app,auxiliary,exploit,information,scanner,shell,tools |less
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

src/pydiesel/api/protobuf_pb2.py: common/protobuf.proto
	cd common; protoc --python_out=../src/pydiesel/api/ protobuf.proto

force: ;
