LOCAL_PATH := $(call my-dir)
 
include $(CLEAR_VARS)
 
LOCAL_MODULE    := exynos-abuse
LOCAL_SRC_FILES := exynos-abuse.c
 
include $(BUILD_EXECUTABLE)
