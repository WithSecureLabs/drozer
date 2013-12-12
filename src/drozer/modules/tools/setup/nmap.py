from drozer.modules import common, Module
import os

class Nmap(Module, common.Shell, common.FileSystem, common.ZipFile, common.ClassLoader):

    name = "Install Nmap."
    description = """Installs Nmap on the Agent.

Nmap ("Network Mapper") is a free and open source (license) utility for network discovery and security auditing.
"""
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2013-12-12"
    license = "BSD (3 clause)"
    path = ["tools", "setup"]

    def execute(self, arguments):

        # ARCH check
        if "ARM" not in str(self.klass('java.lang.System').getProperty("os.arch")).upper():
            response = raw_input("[-] Unsupported CPU architecture - ARM only. Continue anyway (y/n)? ")
            if "Y" not in response.upper():
                return

        folder = self.workingDir() + "/bin/"
        localZip = os.path.join(os.path.dirname(__file__), "nmap-5.51-1.zip")
        remoteZip = folder + "nmap-5.51-1.zip"

        # Remove if it is there
        self.shellExec("rm " + remoteZip)

        if self.ensureDirectory(folder):
            print "[*] Uploading nmap zip"
            bytes_copied = self.uploadFile(localZip, remoteZip)
    
            if bytes_copied != os.path.getsize(localZip):
                print "[-] Failed to upload nmap"
                return
            else:
                print "[+] Uploaded"

            fileList = ["nmap-bin", "nmap-os-db", "nmap-payloads", "nmap-protocols", "nmap-rpc", "nmap-service-probes", "nmap-services", "nmap.test"]
            for file in fileList:
                print "[*] Extracting " + file + "..."
                self.extractFromZip(file, remoteZip, folder)
                self.shellExec("chmod 775 " + folder + file)

            # Write nmap wrapper shell script
            print "[*] Writing nmap wrapper"
            nmap_wrapper = "#!/system/bin/sh\ncd " + folder + "\n./nmap-bin \"$@\""
            self.writeFile(folder + "nmap", nmap_wrapper)
            self.shellExec("chmod 775 " + folder + "nmap")

            print "[+] You can now use nmap from a shell"


