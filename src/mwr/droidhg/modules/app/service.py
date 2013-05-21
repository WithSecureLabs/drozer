from mwr.droidhg import android
from mwr.droidhg.modules import common, Module

class Info(Module, common.Filters, common.PackageManager):

    name = "Get information about exported services"
    description = "Gets information about exported services."
    examples = """List services exported by the Browser:

    mercury> run app.service.info --package com.android.browser
    Package: com.android.browser
      No exported services.

List exported services with no permissions required to interact with it:

    mercury> run app.service.info -p null
    Package: com.android.email
      com.android.email.service.EmailBroadcastProcessorService
        Permission: null
      com.android.email.Controller$ControllerService
        Permission: null
      com.android.email.service.PopImapAuthenticatorService
        Permission: null
      com.android.email.service.PopImapSyncAdapterService
        Permission: null
      com.android.email.service.EasAuthenticatorService
        Permission: null"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "service"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", default=None, help="specify the package to inspect")
        parser.add_argument("-f", "--filter", metavar='<filter>')
        parser.add_argument("-p", "--permission", metavar='<filter>')
        parser.add_argument("-u", "--unexported", action="store_true", default=False, help="include receivers that are not exported")
        parser.add_argument("-v", action="store_true", dest="verbose", default=False)

    def execute(self, arguments):
        if arguments.package == None:
            for package in self.packageManager().getPackages(common.PackageManager.GET_SERVICES | common.PackageManager.GET_PERMISSIONS):
                self.__get_services(arguments, package)
        else:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_SERVICES | common.PackageManager.GET_PERMISSIONS)

            self.__get_services(arguments, package)
            
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "permission":
            return ["null"] + android.permissions

    def __get_services(self, arguments, package):
        services = self.match_filter(package.services, "name", arguments.filter)
        services = self.match_filter(services, "permission", arguments.permission)

        exported_services = self.match_filter(services, "exported", True)
        hidden_services = self.match_filter(services, "exported", False)

        if len(exported_services) > 0 or arguments.unexported and len(services) > 0:
            self.stdout.write("Package: %s\n"%package.packageName)

            if not arguments.unexported:
                for service in exported_services:
                    self.stdout.write("  {}\n".format(service.name))
                    self.stdout.write("    Permission: {}\n".format(service.permission))
            else:
                self.stdout.write("  Exported Services:\n")
                for service in exported_services:
                    self.stdout.write("    {}\n".format(service.name))
                    self.stdout.write("      Permission: {}\n".format(service.permission))
                self.stdout.write("  Hidden Services:\n")
                for service in hidden_services:
                    self.stdout.write("    {}\n".format(service.name))
                    self.stdout.write("      Permission: {}\n".format(service.permission))
            self.stdout.write("\n")
        elif arguments.package or arguments.verbose:
            self.stdout.write("Package: %s\n" % package.packageName)
            self.stdout.write("  No exported services.\n\n")

class Send(Module, common.ServiceBinding):
    
    name = "Send Message"
    description = """Send a message to a service and return a response if any."""

    examples = """
        mercury> run app.service.send com.example.littleapp com.example.littleapp.LittleProvider --  msg 0 0 0 --extra float val 0.1324 --extra string testing testest

        Response Message: 0 0 0
        Data: 
            val (float) : 0.1324
            testing (string) : testest
        

        """
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2013-05-20"
    license = "MWR Code License"
    path = ["app", "service"]
    
    def add_arguments(self, parser):
        parser.add_argument("package", help="Package name")
        parser.add_argument("component", help="Component Name")
        parser.add_argument("--msg", nargs=3, metavar=("what", "arg1", "arg2"), help="message codes")
        parser.add_argument("--extra", nargs=3, metavar=("type","key","value"), action="append", help="elements to be placed in the bundle")
        parser.add_argument("-t", dest="timeout", default="20000", help="specify a timeout in milliseconds (default is 20000)")
        parser.add_argument("-n", dest="no_response", default=False, help="do not wait for a response from the service")

    def execute(self, arguments):

        if arguments.package is None:
            self.stderr.write("Error: Please Specify a Package")
            return
        if arguments.component is None:
            self.stderr.write("Error: Please Specify a Component")
            return
        if arguments.msg is None or len(arguments.msg) is not 3:
            self.stderr.write("Error: messages should be in format \"int int int\"")
            return
        binder = self.getBinding(arguments.package, arguments.component)
    
        if arguments.extra is not None:
            for extra in arguments.extra:
                binder.add_extra(extra)
        else:
            self.stdout.write("No Extras Added\n")

        self.stdout.write("Sending Message\n")
        if arguments.no_response:
            
            binder.send_message(arguments.msg, -1)
        else:
            result = binder.send_message(arguments.msg, arguments.timeout)
            if result:
                ret_message = binder.getMessage();
                ret_bundle = binder.getData();

                self.stdout.write("Response Message: %d %d %d\n" %(int(ret_message.what), int(ret_message.arg1), int(ret_message.arg2)))

                for n in ret_bundle.split('\n'):
                    self.stdout.write("    %s\n"%n)
            else:
                self.stdout.write("Did not get a response from the Service")

    
        
class Start(Module):

    name = "Start Service"
    description = """Formulate an Intent to start a service, and deliver it to another application.

For more information on how to formulate an Intent, type 'help intents'."""
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "service"]

    def add_arguments(self, parser):
        android.Intent.addArgumentsTo(parser)

    def execute(self, arguments):
        intent = android.Intent.fromParser(arguments)
        
        if intent.isValid():        
            self.getContext().startService(intent.buildIn(self))
        else:
            self.stderr.write("invalid intent: one of action or component must be set\n")
    
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest in ["action", "category", "component", "data_uri",
                           "extras", "flags", "mimetype"]:
            return android.Intent.get_completion_suggestions(action, text, **kwargs)

class Stop(Module):

    name = "Stop Service"
    description = "Formulate an Intent to stop a service, and deliver it to another application."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "service"]

    def add_arguments(self, parser):
        android.Intent.addArgumentsTo(parser)

    def execute(self, arguments):
        intent = android.Intent.fromParser(arguments)
        
        if intent.isValid():        
            self.getContext().stopService(intent.buildIn(self))
        else:
            self.stderr.write("invalid intent: one of action or component must be set\n")
    
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest in ["action", "category", "component", "data_uri",
                           "extras", "flags", "mimetype"]:
            return android.Intent.get_completion_suggestions(action, text, **kwargs)
