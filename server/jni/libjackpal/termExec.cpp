/*
 * Copyright (C) 2008 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * Copyright (C) 2007 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * NOTE: MWR InfoSecurity changed the following line of code in this file:
 * static const char *classPathName = "jackpal/androidterm/Exec";
 * to
 * static const char *classPathName = "com/mwr/mercury/Exec";
 */

#define LOG_TAG "Exec"

#include "jni.h"
#include <android/log.h>

#define LOGI(...) do { __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__); } while(0)
#define LOGW(...) do { __android_log_print(ANDROID_LOG_WARN, LOG_TAG, __VA_ARGS__); } while(0)
#define LOGE(...) do { __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__); } while(0)

#include <sys/types.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>
#include <signal.h>

static jclass class_fileDescriptor;
static jfieldID field_fileDescriptor_descriptor;
static jmethodID method_fileDescriptor_init;

typedef unsigned short char16_t;

class String8 {
public:
    String8() {
        mString = 0;
    }

    ~String8() {
        if (mString) {
            free(mString);
        }
    }

    void set(const char16_t* o, size_t numChars) {
        if (mString) {
            free(mString);
        }
        mString = (char*) malloc(numChars + 1);
        if (!mString) {
            return;
        }
        for (size_t i = 0; i < numChars; i++) {
            mString[i] = (char) o[i];
        }
        mString[numChars] = '\0';
    }

    const char* string() {
        return mString;
    }
private:
    char* mString;
};

static int throwOutOfMemoryError(JNIEnv *env, const char *message)
{
    jclass exClass;
    const char *className = "java/lang/OutOfMemoryError";

    exClass = env->FindClass(className);
    return env->ThrowNew(exClass, message);
}

static int create_subprocess(const char *cmd,
    char *const argv[], char *const envp[], int* pProcessId)
{
    char *devname;
    int ptm;
    pid_t pid;

    ptm = open("/dev/ptmx", O_RDWR); // | O_NOCTTY);
    if(ptm < 0){
        LOGE("[ cannot open /dev/ptmx - %s ]\n",strerror(errno));
        return -1;
    }
    fcntl(ptm, F_SETFD, FD_CLOEXEC);

    if(grantpt(ptm) || unlockpt(ptm) ||
       ((devname = (char*) ptsname(ptm)) == 0)){
        LOGE("[ trouble with /dev/ptmx - %s ]\n", strerror(errno));
        return -1;
    }

    pid = fork();
    if(pid < 0) {
        LOGE("- fork failed: %s -\n", strerror(errno));
        return -1;
    }

    if(pid == 0){
        close(ptm);

        int pts;

        setsid();

        pts = open(devname, O_RDWR);
        if(pts < 0) exit(-1);

        dup2(pts, 0);
        dup2(pts, 1);
        dup2(pts, 2);

        if (envp) {
            for (; *envp; ++envp) {
                putenv(*envp);
            }
        }

        execv(cmd, argv);
        exit(-1);
    } else {
        *pProcessId = (int) pid;
        return ptm;
    }
}


static jobject android_os_Exec_createSubProcess(JNIEnv *env, jobject clazz,
    jstring cmd, jobjectArray args, jobjectArray envVars,
    jintArray processIdArray)
{
    const jchar* str = cmd ? env->GetStringCritical(cmd, 0) : 0;
    String8 cmd_8;
    if (str) {
        cmd_8.set(str, env->GetStringLength(cmd));
        env->ReleaseStringCritical(cmd, str);
    }

    jsize size = args ? env->GetArrayLength(args) : 0;
    char **argv = NULL;
    String8 tmp_8;
    if (size > 0) {
        argv = (char **)malloc((size+1)*sizeof(char *));
        if (!argv) {
            throwOutOfMemoryError(env, "Couldn't allocate argv array");
            return NULL;
        }
        for (int i = 0; i < size; ++i) {
            jstring arg = reinterpret_cast<jstring>(env->GetObjectArrayElement(args, i));
            str = env->GetStringCritical(arg, 0);
            if (!str) {
                throwOutOfMemoryError(env, "Couldn't get argument from array");
                return NULL;
            }
            tmp_8.set(str, env->GetStringLength(arg));
            env->ReleaseStringCritical(arg, str);
            argv[i] = strdup(tmp_8.string());
        }
        argv[size] = NULL;
    }

    size = envVars ? env->GetArrayLength(envVars) : 0;
    char **envp = NULL;
    if (size > 0) {
        envp = (char **)malloc((size+1)*sizeof(char *));
        if (!envp) {
            throwOutOfMemoryError(env, "Couldn't allocate envp array");
            return NULL;
        }
        for (int i = 0; i < size; ++i) {
            jstring var = reinterpret_cast<jstring>(env->GetObjectArrayElement(envVars, i));
            str = env->GetStringCritical(var, 0);
            if (!str) {
                throwOutOfMemoryError(env, "Couldn't get env var from array");
                return NULL;
            }
            tmp_8.set(str, env->GetStringLength(var));
            env->ReleaseStringCritical(var, str);
            envp[i] = strdup(tmp_8.string());
        }
        envp[size] = NULL;
    }

    int procId;
    int ptm = create_subprocess(cmd_8.string(), argv, envp, &procId);

    if (argv) {
        for (char **tmp = argv; *tmp; ++tmp) {
            free(*tmp);
        }
        free(argv);
    }
    if (envp) {
        for (char **tmp = envp; *tmp; ++tmp) {
            free(*tmp);
        }
        free(envp);
    }

    if (processIdArray) {
        int procIdLen = env->GetArrayLength(processIdArray);
        if (procIdLen > 0) {
            jboolean isCopy;

            int* pProcId = (int*) env->GetPrimitiveArrayCritical(processIdArray, &isCopy);
            if (pProcId) {
                *pProcId = procId;
                env->ReleasePrimitiveArrayCritical(processIdArray, pProcId, 0);
            }
        }
    }

    jobject result = env->NewObject(class_fileDescriptor, method_fileDescriptor_init);

    if (!result) {
        LOGE("Couldn't create a FileDescriptor.");
    }
    else {
        env->SetIntField(result, field_fileDescriptor_descriptor, ptm);
    }

    return result;
}


static void android_os_Exec_setPtyWindowSize(JNIEnv *env, jobject clazz,
    jobject fileDescriptor, jint row, jint col, jint xpixel, jint ypixel)
{
    int fd;
    struct winsize sz;

    fd = env->GetIntField(fileDescriptor, field_fileDescriptor_descriptor);

    if (env->ExceptionOccurred() != NULL) {
        return;
    }

    sz.ws_row = row;
    sz.ws_col = col;
    sz.ws_xpixel = xpixel;
    sz.ws_ypixel = ypixel;

    ioctl(fd, TIOCSWINSZ, &sz);
}

static int android_os_Exec_waitFor(JNIEnv *env, jobject clazz,
    jint procId) {
    int status;
    waitpid(procId, &status, 0);
    int result = 0;
    if (WIFEXITED(status)) {
        result = WEXITSTATUS(status);
    }
    return result;
}

static void android_os_Exec_close(JNIEnv *env, jobject clazz, jobject fileDescriptor)
{
    int fd;

    fd = env->GetIntField(fileDescriptor, field_fileDescriptor_descriptor);

    if (env->ExceptionOccurred() != NULL) {
        return;
    }

    close(fd);
}

static void android_os_Exec_hangupProcessGroup(JNIEnv *env, jobject clazz,
    jint procId) {
    kill(-procId, SIGHUP);
}


static int register_FileDescriptor(JNIEnv *env)
{
    jclass localRef_class_fileDescriptor = env->FindClass("java/io/FileDescriptor");

    if (localRef_class_fileDescriptor == NULL) {
        LOGE("Can't find class java/io/FileDescriptor");
        return -1;
    }

    class_fileDescriptor = (jclass) env->NewGlobalRef(localRef_class_fileDescriptor);

    env->DeleteLocalRef(localRef_class_fileDescriptor);

    if (class_fileDescriptor == NULL) {
        LOGE("Can't get global ref to class java/io/FileDescriptor");
        return -1;
    }

    field_fileDescriptor_descriptor = env->GetFieldID(class_fileDescriptor, "descriptor", "I");

    if (field_fileDescriptor_descriptor == NULL) {
        LOGE("Can't find FileDescriptor.descriptor");
        return -1;
    }

    method_fileDescriptor_init = env->GetMethodID(class_fileDescriptor, "<init>", "()V");
    if (method_fileDescriptor_init == NULL) {
        LOGE("Can't find FileDescriptor.init");
        return -1;
     }
     return 0;
}


static const char *classPathName = "com/mwr/mercury/Exec";

static JNINativeMethod method_table[] = {
    { "createSubprocess", "(Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/String;[I)Ljava/io/FileDescriptor;",
        (void*) android_os_Exec_createSubProcess },
    { "setPtyWindowSize", "(Ljava/io/FileDescriptor;IIII)V",
        (void*) android_os_Exec_setPtyWindowSize},
    { "waitFor", "(I)I",
        (void*) android_os_Exec_waitFor},
    { "close", "(Ljava/io/FileDescriptor;)V",
        (void*) android_os_Exec_close},
    { "hangupProcessGroup", "(I)V",
        (void*) android_os_Exec_hangupProcessGroup}
};

/*
 * Register several native methods for one class.
 */
static int registerNativeMethods(JNIEnv* env, const char* className,
    JNINativeMethod* gMethods, int numMethods)
{
    jclass clazz;

    clazz = env->FindClass(className);
    if (clazz == NULL) {
        LOGE("Native registration unable to find class '%s'", className);
        return JNI_FALSE;
    }
    if (env->RegisterNatives(clazz, gMethods, numMethods) < 0) {
        LOGE("RegisterNatives failed for '%s'", className);
        return JNI_FALSE;
    }

    return JNI_TRUE;
}

/*
 * Register native methods for all classes we know about.
 *
 * returns JNI_TRUE on success.
 */
static int registerNatives(JNIEnv* env)
{
  if (!registerNativeMethods(env, classPathName, method_table,
                 sizeof(method_table) / sizeof(method_table[0]))) {
    return JNI_FALSE;
  }

  return JNI_TRUE;
}


// ----------------------------------------------------------------------------

/*
 * This is called by the VM when the shared library is first loaded.
 */

typedef union {
    JNIEnv* env;
    void* venv;
} UnionJNIEnvToVoid;

jint JNI_OnLoad(JavaVM* vm, void* reserved) {
    UnionJNIEnvToVoid uenv;
    uenv.venv = NULL;
    jint result = -1;
    JNIEnv* env = NULL;

    LOGI("JNI_OnLoad");

    if (vm->GetEnv(&uenv.venv, JNI_VERSION_1_4) != JNI_OK) {
        LOGE("ERROR: GetEnv failed");
        goto bail;
    }
    env = uenv.env;

    if ((result = register_FileDescriptor(env)) < 0) {
        LOGE("ERROR: registerFileDescriptor failed");
        goto bail;
    }

    if (registerNatives(env) != JNI_TRUE) {
        LOGE("ERROR: registerNatives failed");
        goto bail;
    }

    result = JNI_VERSION_1_4;

bail:
    return result;
}
