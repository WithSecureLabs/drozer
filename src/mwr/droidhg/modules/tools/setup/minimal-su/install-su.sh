#!/system/bin/sh

mount -o remount,rw -t yaffs2 /system
cat /data/data/com.mwr.droidhg.agent/su > /system/bin/su
chmod 4755 /system/bin/su
echo 'Done. You can now use `su` from a shell.'
