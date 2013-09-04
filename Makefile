
NATIVES = $(shell find src/drozer/modules -name Android.mk)
SOURCES = $(shell find src/drozer/modules -name *.java)

DX = dx
JAVAC = javac
NDKBUILD = ndk-build
PYTHON = python

SDK = $(CURDIR)/src/drozer/lib/android.jar

all: sources apks native-libraries
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

force: ;
