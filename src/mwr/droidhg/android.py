
class Intent(object):
    """
    Representation of an Android Intent object in Python.

    An Python representation of an Intent can be built, and then converted into
    a Java representation using the buildIn() method to add context.
    """

    actions = [     'android.intent.action.ACTION_MAIN',
                    'android.intent.action.ACTION_VIEW',
                    'android.intent.action.ACTION_ATTACH_DATA',
                    'android.intent.action.ACTION_EDIT',
                    'android.intent.action.ACTION_PICK',
                    'android.intent.action.ACTION_CHOOSER',
                    'android.intent.action.ACTION_GET_CONTENT',
                    'android.intent.action.ACTION_DIAL',
                    'android.intent.action.ACTION_CALL',
                    'android.intent.action.ACTION_SEND',
                    'android.intent.action.ACTION_SENDTO',
                    'android.intent.action.ACTION_ANSWER',
                    'android.intent.action.ACTION_INSERT',
                    'android.intent.action.ACTION_DELETE',
                    'android.intent.action.ACTION_RUN',
                    'android.intent.action.ACTION_SYNC',
                    'android.intent.action.ACTION_PICK_ACTIVITY',
                    'android.intent.action.ACTION_SEARCH',
                    'android.intent.action.ACTION_WEB_SEARCH',
                    'android.intent.action.ACTION_FACTORY_TEST',
                    'android.intent.action.ACTION_TIME_TICK',
                    'android.intent.action.ACTION_TIME_CHANGED',
                    'android.intent.action.ACTION_TIMEZONE_CHANGED',
                    'android.intent.action.ACTION_BOOT_COMPLETED',
                    'android.intent.action.ACTION_PACKAGE_ADDED',
                    'android.intent.action.ACTION_PACKAGE_CHANGED',
                    'android.intent.action.ACTION_PACKAGE_REMOVED',
                    'android.intent.action.ACTION_PACKAGE_RESTARTED',
                    'android.intent.action.ACTION_PACKAGE_DATA_CLEARED',
                    'android.intent.action.ACTION_UID_REMOVED',
                    'android.intent.action.ACTION_BATTERY_CHANGED',
                    'android.intent.action.ACTION_POWER_CONNECTED',
                    'android.intent.action.ACTION_POWER_DISCONNECTED',
                    'android.intent.action.ACTION_SHUTDOWN' ]
    categories = [  'android.intent.category.CATEGORY_DEFAULT',
                    'android.intent.category.CATEGORY_BROWSABLE',
                    'android.intent.category.CATEGORY_TAB',
                    'android.intent.category.CATEGORY_ALTERNATIVE',
                    'android.intent.category.CATEGORY_SELECTED_ALTERNATIVE',
                    'android.intent.category.CATEGORY_LAUNCHER',
                    'android.intent.category.CATEGORY_INFO',
                    'android.intent.category.CATEGORY_HOME',
                    'android.intent.category.CATEGORY_PREFERENCE',
                    'android.intent.category.CATEGORY_TEST',
                    'android.intent.category.CATEGORY_CAR_DOCK',
                    'android.intent.category.CATEGORY_DESK_DOCK',
                    'android.intent.category.CATEGORY_LE_DESK_DOCK',
                    'android.intent.category.CATEGORY_HE_DESK_DOCK',
                    'android.intent.category.CATEGORY_CAR_MODE',
                    'android.intent.category.CATEGORY_APP_MARKET' ]
    extra_keys = [  'android.intent.extra.EXTRA_ALARM_COUNT',
                    'android.intent.extra.EXTRA_BCC',
                    'android.intent.extra.EXTRA_CC',
                    'android.intent.extra.EXTRA_CHANGED_COMPONENT_NAME',
                    'android.intent.extra.EXTRA_DATA_REMOVED',
                    'android.intent.extra.EXTRA_DOCK_STATE',
                    'android.intent.extra.EXTRA_DOCK_STATE_HE_DESK',
                    'android.intent.extra.EXTRA_DOCK_STATE_LE_DESK',
                    'android.intent.extra.EXTRA_DOCK_STATE_CAR',
                    'android.intent.extra.EXTRA_DOCK_STATE_DESK',
                    'android.intent.extra.EXTRA_DOCK_STATE_UNDOCKED',
                    'android.intent.extra.EXTRA_DONT_KILL_APP',
                    'android.intent.extra.EXTRA_EMAIL',
                    'android.intent.extra.EXTRA_INITIAL_INTENTS',
                    'android.intent.extra.EXTRA_INTENT',
                    'android.intent.extra.EXTRA_KEY_EVENT',
                    'android.intent.extra.EXTRA_ORIGINATING_URI',
                    'android.intent.extra.EXTRA_PHONE_NUMBER',
                    'android.intent.extra.EXTRA_REFERRER',
                    'android.intent.extra.EXTRA_REMOTE_INTENT_TOKEN',
                    'android.intent.extra.EXTRA_REPLACING',
                    'android.intent.extra.EXTRA_SHORTCUT_ICON',
                    'android.intent.extra.EXTRA_SHORTCUT_ICON_RESOURCE',
                    'android.intent.extra.EXTRA_SHORTCUT_INTENT',
                    'android.intent.extra.EXTRA_STREAM',
                    'android.intent.extra.EXTRA_SHORTCUT_NAME',
                    'android.intent.extra.EXTRA_SUBJECT',
                    'android.intent.extra.EXTRA_TEMPLATE',
                    'android.intent.extra.EXTRA_TEXT',
                    'android.intent.extra.EXTRA_TITLE',
                    'android.intent.extra.EXTRA_UID' ]
    extra_types = [ 'boolean',
                    'byte',
                    'char',
                    'double',
                    'float',
                    'integer',
                    'long',
                    'parcelable',
                    'short',
                    'string' ]
    flags = {       'ACTIVITY_BROUGHT_TO_FRONT': 0x00400000,
                    'ACTIVITY_CLEAR_TASK': 0x00008000,
                    'ACTIVITY_CLEAR_TOP': 0x04000000,
                    'ACTIVITY_CLEAR_WHEN_TASK_RESET': 0x00080000,
                    'ACTIVITY_EXCLUDE_FROM_RECENTS': 0x00800000,
                    'ACTIVITY_FORWARD_RESULT': 0x02000000,
                    'ACTIVITY_LAUNCHED_FROM_HISTORY': 0x00100000,
                    'ACTIVITY_MULTIPLE_TASK': 0x08000000,
                    'ACTIVITY_NEW_TASK': 0x10000000,
                    'ACTIVITY_NO_ANIMATION': 0x00010000,
                    'ACTIVITY_NO_HISTORY': 0x40000000,
                    'ACTIVITY_NO_USER_ACTION': 0x00040000,
                    'ACTIVITY_PREVIOUS_IS_TOP': 0x01000000,
                    'ACTIVITY_REORDER_TO_FRONT': 0x00020000,
                    'ACTIVITY_RESET_TASK_IF_NEEDED': 0x00200000,
                    'ACTIVITY_SINGLE_TOP': 0x20000000,
                    'ACTIVITY_TASK_ON_HOME': 0x00004000,
                    'FLAG_DEBUG_LOG_RESOLUTION': 0x00000008,
                    'FROM_BACKGROUND': 0x00000004,
                    'GRANT_READ_URI_PERMISSION': 0x00000001,
                    'GRANT_WRITE_URI_PERMISSION': 0x00000002,
                    'RECEIVER_REGISTERED_ONLY': 0x40000000 }

    def __init__(self, action=None, category=None, component=None,
        data_uri=None, extras=None, flags=None, mimetype=None):
        self.action = action
        self.category = category
        self.component = component
        self.data_uri = data_uri
        self.extras = extras
        self.flags = flags
        self.mimetype = mimetype

    @classmethod
    def addArgumentsTo(cls, parser):
        """
        Prepares an ArgumentParser object to allow a user to pass Intent
        arguments through a command-line interface.
        """

        parser.add_argument("--action", help="specify the action to include in the Intent")
        parser.add_argument("--category", help="specify the category to include in the Intent")
        parser.add_argument("--component", help="specify the component name to include in the Intent", nargs=2)
        parser.add_argument("--data-uri", help="specify a Uri to attach as data in the Intent")
        parser.add_argument("--extra", action="append", default=[],
            dest="extras", nargs=3, help="add an field to the Intent's extras bundle", metavar=('type', 'key', 'value'))
        parser.add_argument("--flags", nargs='+', default=[], help="specify one-or-more flags to include in the Intent")
        parser.add_argument("--mimetype", help="specify the MIME type to send in the Intent")

    @classmethod
    def fromParser(cls, arguments):
        """
        Builds an Intent, given arguments parsed by an ArgumentParser that was
        previously initialised with addArgumentsTo().
        """

        return cls( action=arguments.action,
                    category=arguments.category,
                    component=arguments.component,
                    data_uri=arguments.data_uri,
                    extras=arguments.extras,
                    flags=arguments.flags,
                    mimetype=arguments.mimetype)
        
    @classmethod
    def get_completion_suggestions(cls, action, text, **kwargs):
        """
        Provide completion suggestions for Android Intents.
        """
        
        if action.dest == "action":
            return cls.actions
        elif action.dest == "category":
            return cls.categories
        elif action.dest == "component":
            pass
        elif action.dest == "data_uri":
            pass
        elif action.dest == "extras":
            if kwargs['idx'] == 0:
                return cls.extra_types
            elif kwargs['idx'] == 1:
                return cls.extra_keys
        elif action.dest == "flags":
            return cls.flags.keys()
        elif action.dest == "mimetype":
            pass

    def buildIn(self, module):
        """
        Convert a Python Intent representation into a Java Intent that can be
        used with reflection, by adding context.
        """

        intent = module.new("android.content.Intent")

        self.__add_action_to(intent, module)
        self.__add_category_to(intent, module)
        self.__add_component_to(intent, module)
        self.__add_data_uri_to(intent, module)
        self.__add_extras_to(intent, module)
        self.__add_flags_to(intent, module)
        self.__add_type_to(intent, module)

        return intent

    def isValid(self):
        """
        Determine whether an Intent is valid: it must have an action or a
        component.
        """

        return self.action != None or self.component != None
    
    def __add_action_to(self, intent, context):
        """
        Set the ACTION of intent, iff we have a value to set.
        """
        
        if self.action != None:
            intent.setAction(self.action)
    
    def __add_category_to(self, intent, context):
        """
        Set the CATEGORY of intent, iff we have a value to set.
        """
        
        if self.category != None:
            intent.addCategory(self.category)
    
    def __add_component_to(self, intent, context):
        """
        Set the COMPONENT of intent, iff we have a value to set.
        """
        
        if self.component != None:
            com = context.new("android.content.ComponentName", *self.component)
            # pass the built ComponentName to the intent
            intent.setComponent(com)
    
    def __add_data_uri_to(self, intent, context):
        """
        Set the DATA of intent as a Uri, iff we have a value to set.
        """
        
        if self.data_uri != None:
            uri = context.klass("android.net.Uri")
            intent.setData(uri.parse(self.data_uri))

    def __add_extras_to(self, intent, context):
        """
        Set the EXTRAS of intent, iff we have a value to set.
        """
        
        if self.extras != None:
            extras = context.new("android.os.Bundle")

            for extra in self.extras:
                if extra[0] == "boolean":
                    extras.putBoolean(extra[1], extra[2])
                elif extra[0] == "byte":
                    extras.putByte(extra[1], extra[2])
                elif extra[0] == "char":
                    extras.putChar(extra[1], extra[2])
                elif extra[0] == "double":
                    extras.putDouble(extra[1], extra[2])
                elif extra[0] == "float":
                    extras.putFloat(extra[1], extra[2])
                elif extra[0] == "integer":
                    extras.putInt(extra[1], extra[2])
                elif extra[0] == "long":
                    extras.putLong(extra[1], extra[2])
                elif extra[0] == "short":
                    extras.putShort(extra[1], extra[2])
                elif extra[0] == "string":
                    extras.putString(extra[1], extra[2])
                else:
                    extras.putParcelable(extra[1], extra[2])

            intent.putExtras(extras)
            
    def __add_flags_to(self, intent, context):
        """
        Set the FLAGS of intent, iff we have a value to set.
        """
        if self.flags != None:
            intent.setFlags(self.__build_flags(self.flags))
    
    def __add_type_to(self, intent, context):
        """
        Set the TYPE of intent, iff we have a value to set.
        """
        
        if self.mimetype != None:
            intent.setType(self.mimetype)
            
    def __build_flags(self, flags):
        """
        Take arguments passed as flags, and combine them to form the integer
        flag field to pass in an Intent.

        We can accept flags either as a key from the flags dictionary above,
        or in a binary format.
        """

        flag = 0x00000000

        for flag_spec in flags:
            if flag_spec.startswith("0x"):
                flag = flag | int(flag_spec[2:], 16) # support hexadecimal flags
            else:
                flag = flag | self.__class__.flags[flag_spec]

        return flag
        