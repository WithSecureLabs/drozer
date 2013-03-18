from mwr.droidhg import android
from mwr.droidhg.modules import common, Module

class ForIntent(Module, common.PackageManager):

    name = "Find activities that can handle the given intent"
    description = "Find activities that can handle the formulated intent"
    examples = """Find activities that can handle web addresses:

    mercury> run app.activity.forintent
                --action android.intent.action.VIEW
                --data http://www.google.com

    Package name: com.android.browser
    Target activity: com.android.browser.BrowserActivity"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "activity"]

    def add_arguments(self, parser):
        android.Intent.addArgumentsTo(parser)

    def execute(self, arguments):
        intent = android.Intent.fromParser(arguments)

        if intent.isValid():
            for activity in self.packageManager().queryIntentActivities(intent, common.PackageManager.MATCH_DEFAULT_ONLY | common.PackageManager.GET_ACTIVITIES | common.PackageManager.GET_INTENT_FILTERS | common.PackageManager.GET_RESOLVED_FILTER):
                activity_info = activity.activityInfo

                self.stdout.write("Package: %s\n" % activity_info.packageName)
                self.stdout.write("  %s\n\n" % activity_info.name)
        else:
            self.stderr.write("invalid intent: one of action or component must be set\n")
    
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest in ["action", "category", "component", "data_uri",
                           "extras", "flags", "mimetype"]:
            return android.Intent.get_completion_suggestions(action, text, **kwargs)

class Info(Module, common.Filters, common.PackageManager):
    
    name = "Gets information about exported activities."
    description = "Gets information about exported activities."
    examples = """List activities exported by the Browser:

    mercury> run app.activity.info --package com.android.browser
    Package: com.android.browser
      com.android.browser.BrowserActivity
      com.android.browser.ShortcutActivity
      com.android.browser.BrowserPreferencesPage
      com.android.browser.BookmarkSearch
      com.android.browser.AddBookmarkPage
      com.android.browser.widget.BookmarkWidgetConfigure"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "activity"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", default=None, help="specify the package to inspect")
        parser.add_argument("-f", "--filter", default=None, help="specify a filter term for the activity name")
        parser.add_argument("-u", "--unexported", action="store_true", default=False, help="include activities that are not exported")
        parser.add_argument("-v", "--verbose", action="store_true", default=False, help="be verbose")

    def execute(self, arguments):
        if arguments.package == None:
            for package in self.packageManager().getPackages(common.PackageManager.GET_ACTIVITIES):
                self.__get_activities(arguments, package)
        else:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_ACTIVITIES)

            self.__get_activities(arguments, package)

    def __get_activities(self, arguments, package):
        activities = self.match_filter(package.activities, 'name', arguments.filter)

        exported_activities = self.match_filter(activities, 'exported', True)
        hidden_activities = self.match_filter(activities, 'exported', False)

        if len(exported_activities) > 0 or arguments.unexported and len(activities) > 0:
            self.stdout.write("Package: %s\n" % package.packageName)

            if not arguments.unexported:
                for activity in exported_activities:
                    self.stdout.write("  %s\n" % activity.name)
            else:
                self.stdout.write("  Exported Activities:\n")
                for activity in exported_activities:
                    self.stdout.write("    %s\n" % activity.name)
                self.stdout.write("  Hidden Activities:\n")
                for activity in hidden_activities:
                    self.stdout.write("    %s\n" % activity.name)
            self.stdout.write("\n")
        elif arguments.package or arguments.verbose:
            self.stdout.write("Package: %s\n" % package.packageName)
            self.stdout.write("  No matching activities.\n\n")
                
class Start(Module):

    name = "Start an Activity"
    description = "Starts an Activity using the formulated intent."
    examples = """Start the Browser with an explicit intent:

    mercury> run app.activity.start
                --component com.android.browser
                            com.android.browser.BrowserActivity
                --flags ACTIVITY_NEW_TASK

Starting the Browser with an implicit intent:

    mercury> run app.activity.start
                --action android.intent.action.VIEW
                --data-uri http://www.google.com
                --flags ACTIVITY_NEW_TASK"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "activity"]

    def add_arguments(self, parser):
        android.Intent.addArgumentsTo(parser)

    def execute(self, arguments):
        intent = android.Intent.fromParser(arguments)

        if intent.isValid():
            self.getContext().startActivity(intent.buildIn(self))
        else:
            self.stderr.write("invalid intent: one of action or component must be set\n")
    
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest in ["action", "category", "component", "data_uri",
                           "extras", "flags", "mimetype"]:
            return android.Intent.get_completion_suggestions(action, text, **kwargs)
            