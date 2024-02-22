LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

LOCAL_MODULE := WebViewContext
LOCAL_SRC_FILES := main.c

LOCAL_C_INCLUDES := dalvik
LOCAL_STATIC_LIBRARIES := libdex
LOCAL_SHARED_LIBRARIES := libcutils
LOCAL_LDLIBS := -L$(SYSROOT)/usr/lib -llog

include $(BUILD_SHARED_LIBRARY)