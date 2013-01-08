from mwr.droidhg.modules import common, Module

class Su(Module, common.ClassLoader, common.FileSystem, common.Shell, common.SuperUser):

    name = "Prepare su binary installation on the device."
    description = """Prepares su binary installation files on the device in order to provide access to a root shell on demand.

This binary provides Mercury the ability to maintain access to a root shell on the device after obtaining a temporary root shell via the use of an exploit. Just type `su` from a shell to get a root shell.

WARNING: This minimal version of the su binary is completely unprotected, meaning that any application on the device can obtain a root shell without any user prompting.
"""
    examples = """
    mercury> run tools.setup.su
    [*] Uploaded su
    [*] Uploaded install-su.sh
    [*] chmod 770 /data/data/com.mwr.droidhg.agent/install-su.sh
    [*] Ready! Execute /data/data/com.mwr.droidhg.agent/install-su.sh from root context to install su
    
    ...insert root exploit here...
    u0_a95@android:/data/data/com.mwr.droidhg.agent # /data/data/com.mwr.droidhg.agent/install-su.sh
    Done. You can now use `su` from a shell.
    u0_a95@android:/data/data/com.mwr.droidhg.agent # exit
    u0_a95@android:/data/data/com.mwr.droidhg.agent $ su
    u0_a95@android:/data/data/com.mwr.droidhg.agent #
    """
    author = "Tyrone (@mwrlabs)"
    date = "2013-01-08"
    license = "MWR Code License"
    path = ["tools", "setup"]

    def execute(self, arguments):
        
        # Check for existence of /system/bin/su
        if self.isSuInstalled():
            self.stdout.write("[!] A version of su is already installed at /system/bin/su\n")
        
        # Upload su binary
        if self.uploadSu():
            self.stdout.write("[*] Uploaded su\n")
        else:
            self.stdout.write("[-] Upload failed (su) - aborting\n")
            return
        
        # Upload install-su.sh    
        if self.uploadSuInstallScript():
            self.stdout.write("[*] Uploaded install-su.sh\n")
            self.stdout.write("[*] chmod 770 /data/data/com.mwr.droidhg.agent/install-su.sh\n")
        else:
            self.stdout.write("[-] Upload failed (install-su.sh) - aborting\n")
            return
        
        # Ready to be used from root context
        self.stdout.write("[*] Ready! Execute /data/data/com.mwr.droidhg.agent/install-su.sh from root context to install su\n")

