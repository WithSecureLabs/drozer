LOCAL_PATH := $(call my-dir)
 
include $(CLEAR_VARS)
 
# Here we give our module name and source file(s)
LOCAL_MODULE    := su
LOCAL_SRC_FILES := su.c
 
include $(BUILD_EXECUTABLE)
