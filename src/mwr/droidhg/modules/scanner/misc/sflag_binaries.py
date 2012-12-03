from mwr.droidhg.modules import common, Module

class SFlagBinaries(Module, common.BusyBox, common.ClassLoader, common.FileSystem, common.Shell):

    name = "Find suid/sgid binaries in the /system folder."
    description = "Find suid/sgid binaries in the /system folder. Uses the method from http://hexesec.wordpress.com/2009/10/14/exploiting-suid-binaries/."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["scanner", "misc"]

    def execute(self, arguments):
        if self.isBusyBoxInstalled():
            binaries = self.busyBoxExec("find /system -type f \( -perm -04000 -o -perm -02000 \) \-exec ls {} \;")
            sflag_binaries = []

            for binary in iter(binaries.split("\n")):
                if not binary.startswith('find: '):
                    sflag_binaries.append(binary)

            if len(sflag_binaries) > 0:
                self.stdout.write("Found suid/sgid binaries:\n")
                for binary in sflag_binaries:
                    self.stdout.write("  %s\n" % binary)
            else:
                self.stdout.write("No suid/sguid binaries.")
        else:
            self.stderr.write("This command requires BusyBox to complete. Run tools.setup.busybox and then retry.\n")
