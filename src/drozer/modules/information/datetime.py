from drozer.modules import Module

class DateTime(Module):

    name = "Print Date/Time"
    description = "Retrieves the current date and time from the Android device."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["information"]

    def execute(self, arguments):
        time = self.new("android.text.format.Time")
        time.setToNow()

        self.stdout.write("The time is %s.\n" % time.format2445())
        
