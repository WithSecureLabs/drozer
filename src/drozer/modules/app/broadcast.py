from xml.etree import ElementTree

from drozer import android
from drozer.modules import common, Module

class Info(Module, common.Filters, common.IntentFilter, common.PackageManager):

    name = "Get information about broadcast receivers"
    description = "Get information about exported broadcast receivers."
    examples = """Get receivers exported by the platform:

    dz> run app.broadcast.info -a android
    Package: android
      Receiver: com.android.server.BootReceiver
        Intent Filters:
        Permission: null
      Receiver: com.android.server.MasterClearReceiver
        Intent Filters:
        Permission: android.permission.MASTER_CLEAR"""
    author = ["MWR InfoSecurity (@mwrlabs)", "Luander (luander.r@samsung.com)"]
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["app", "broadcast"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", default=None, help="specify the package to inspect")
        parser.add_argument("-f", "--filter", default=None, help="specify filter conditions")
        parser.add_argument("-p", "--permission", default=None, help="specify permission conditions")
        parser.add_argument("-i", "--show-intent-filters", action="store_true", default=False, help="specify whether to include intent filters")
        parser.add_argument("-u", "--unexported", action="store_true", default=False, help="include receivers that are not exported")
        parser.add_argument("-v", "--verbose", action="store_true", default=False, help="be verbose")

    def execute(self, arguments):
        if arguments.package == None:
            for package in self.packageManager().getPackages(common.PackageManager.GET_RECEIVERS | common.PackageManager.GET_PERMISSIONS):
                self.__get_receivers(arguments, package)
        else:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_RECEIVERS | common.PackageManager.GET_PERMISSIONS)

            self.__get_receivers(arguments, package)
            
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "permission":
            return ["null"] + android.permissions

    def __get_receivers(self, arguments, package):
        receivers = self.match_filter(package.receivers, 'name', arguments.filter)
        receivers = self.match_filter(receivers, 'permission', arguments.permission)

        exported_receivers = self.match_filter(receivers, 'exported', True)
        hidden_receivers = self.match_filter(receivers, 'exported', False)

        if len(exported_receivers) > 0 or arguments.unexported and len(receivers) > 0:
            self.stdout.write("Package: %s\n" % package.packageName)

            if not arguments.unexported:
                for receiver in exported_receivers:
                    self.__print_receiver(package, receiver, "  ", arguments.show_intent_filters)
            else:
                self.stdout.write("  Exported Receivers:\n")
                for receiver in exported_receivers:
                    self.__print_receiver(package, receiver, "    ", arguments.show_intent_filters)
                self.stdout.write("  Hidden Receivers:\n")
                for receiver in hidden_receivers:
                    self.__print_receiver(package, receiver, "    ", arguments.show_intent_filters)
            self.stdout.write("\n")
        elif arguments.package or arguments.verbose:
            self.stdout.write("Package: %s\n" % package.packageName)
            self.stdout.write("  No matching receivers.\n\n")

    def __print_receiver(self, package, receiver, prefix, include_intent_filters=False):
        self.stdout.write("%sReceiver: %s\n" % (prefix, receiver.name))
            
        if include_intent_filters:
            intent_filters = self.find_intent_filters(receiver, 'receiver')
            
            if len(intent_filters) > 0:
                for intent_filter in intent_filters:
                    self.stdout.write("%s  Intent Filter:\n" % (prefix))
                    if len(intent_filter.actions) > 0:
                        self.stdout.write("%s    Actions:\n" % (prefix))
                        for action in intent_filter.actions:
                            self.stdout.write("%s      - %s\n" % (prefix, action))
                    if len(intent_filter.categories) > 0:
                        self.stdout.write("%s    Categories:\n" % (prefix))
                        for category in intent_filter.categories:
                            self.stdout.write("%s      - %s\n" % (prefix, category))
                    if len(intent_filter.datas) > 0:
                        self.stdout.write("%s    Data:\n" % (prefix))
                        for data in intent_filter.datas:
                            self.stdout.write("%s      - %s\n" % (prefix, data))
            self.stdout.write("%s  Permission: %s\n" % (prefix, receiver.permission))

class Send(Module):

    name = "Send broadcast using an intent"
    description = "Sends an intent to broadcast receivers."
    examples = """Attempt to send the BOOT_COMPLETED broadcast message:

    dz> run app.broadcast.send
                --action android.intent.action.BOOT_COMPLETED
    java.lang.SecurityException: Permission Denial: not allowed to send broadcast android.intent.action.BOOT_COMPLETED from pid=955, uid=10044

For more information on how to formulate an Intent, type 'help intents'."""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["app", "broadcast"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def add_arguments(self, parser):
        android.Intent.addArgumentsTo(parser)

    def execute(self, arguments):
        intent = android.Intent.fromParser(arguments)

        if intent.isValid():
            self.getContext().sendBroadcast(intent.buildIn(self))
        else:
            self.stderr.write("invalid intent: one of action or component must be set")
    
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest in ["action", "category", "component", "data_uri",
                           "extras", "flags", "mimetype"]:
            return android.Intent.get_completion_suggestions(action, text, **kwargs)
            
