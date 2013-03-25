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
                for service in services:
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
