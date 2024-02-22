/*

Made by metall0id (Tyrone @mwrlabs)

mount -o remount,rw -t yaffs2 /system
cat su > /system/bin/su
chmod 4755 /system/bin/su

*/

#include <stdio.h>
#include <unistd.h>

int main(int argc, char **argv)
{
	if (setgid(0) || setuid(0))
		fprintf(stderr, "su: permission denied\n");
	else
	{
		char *args[argc + 1];
		args[0] = "sh";
		args[argc] = NULL;
		
		int i;
		for (i = 1; i < argc; i++)
		        args[i] = argv[i];

		execv("/system/bin/sh", args);
	}
}

