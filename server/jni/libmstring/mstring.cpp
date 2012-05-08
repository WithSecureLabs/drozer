/*
 * mstring.cpp
 *
 * Written by Rodrigo Chiossi.
 *
 * Buffered String Search	<r.chiossi@samsung.com>
 */

/*
 * ABOUT THE CODE:
 *
 * This is a native implementation of a buffered string search algorithm,
 * optimized to reduce the overhead of the JNI call.
 *
 * The number of strings found is usually very big which makes it impossible
 * return a list of jstrings objects back to java (due to the restriction of
 * 512 local references) without paying the price of DeleteLocalRef().
 *
 * This implementation creates a single Java string with all strings separated
 * by a new line. An actual list can be then retrieved in Java using
 * split("\n"), or any method alike.
 *
 * The chunk size was obtained by profiling the execution time over several
 * classes.dex extracted from apks. The best observed value was 16k.
 */

#include <jni.h>  
#include <string.h>  
#include <android/log.h>  
#include <stdlib.h>
#include <stdio.h>
  
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR  , "mercury-native", __VA_ARGS__)

#ifdef __cplusplus
extern "C" {
#endif

#define CHUNK_SIZE 16348
#define LIST_START_SIZE 4096

#define MAX_STR_SIZE 4096
#define MIN_STR_SIZE 4

char read_buffer[CHUNK_SIZE];
unsigned bytes_in_buffer;
unsigned read_ptr;
unsigned eof;

char* string_list = NULL;

/*
 * Function: Read a new chunk from the target file
 * Parameters:  file - open file descriptor to the target
 */
void reset_buffer(FILE* file) {
	bytes_in_buffer = fread(read_buffer,1,CHUNK_SIZE,file);
	read_ptr = 0;
	eof = 0;
}

/*
 * Function: Read a byte from the file buffer
 * Parameters:  file - open file descriptor to the target
 * Return: Byte read
 */
char read_char(FILE* file) {
	if (bytes_in_buffer != CHUNK_SIZE && read_ptr >= bytes_in_buffer) {
		eof = 1;
		return 0xff;
	}

	if (read_ptr == CHUNK_SIZE) {
		reset_buffer(file);
	}

	return read_buffer[read_ptr++];
}

/*
 * Function: Extract Strings from file
 * Parameters:  path - taget file
 * Return: Number of uris found
 */
int strings_file(const char* path) {
	FILE* file = fopen(path,"r");

	unsigned max_size = LIST_START_SIZE;
	unsigned cur_size = 0;

	char buffer[MAX_STR_SIZE];
	char* next_str;
	unsigned char c_byte;
	unsigned length;

	unsigned num_strings = 0;

	if (file == NULL) {
		LOGE("Error opening file : %s",path);
		return -1;
	}

	string_list = (char*) malloc(sizeof(char)*max_size);

	reset_buffer(file);

	c_byte = read_char(file);
	length = 0;
	while (!eof) {
		/* check if character is printable */
		while (0x20 <= c_byte && c_byte <= 0x7E && length < MAX_STR_SIZE - 1 && !eof) {
			buffer[length++] = c_byte;
			c_byte = read_char(file);
		}

		if (length >= MIN_STR_SIZE) {
			/* grow string list buffer if needed */
			if (cur_size+length >= max_size) {
				string_list = (char*) realloc(string_list, sizeof(char)*max_size*2);
				if (string_list == NULL) {
					LOGE("Error: Failed to allocate memory!");
					return -1;
				}
				max_size *= 2;
			}

			next_str = &string_list[cur_size];
			strncpy(next_str,buffer,length);
			next_str[length] = '\n';

			cur_size+=length+1;

			num_strings++;
		}

		/* start a new string */
		length = 0;

		c_byte = read_char(file);
	}

	fclose(file);

	return num_strings;
}

/*
 * Class:     com_mwr_mercury_Common
 * Method:    native_strings
 * Signature: (Ljava/lang/String;)[Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_com_mwr_mercury_Common_native_1strings
  (JNIEnv *env, jclass obj, jstring jpath)
{
	const char *path = env->GetStringUTFChars(jpath, 0);
	int num;

	/* Get string list */
	num = strings_file(path);

	if (num <= 0) return NULL;

	/* Convert to a Java String */
	env->ReleaseStringUTFChars(jpath, path);
	jstring ret = env->NewStringUTF(string_list);

	free(string_list);

	return ret;
}

#ifdef __cplusplus
}
#endif
