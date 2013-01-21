
class Intent(object):
    """
    Representation of an Android Intent object in Python.

    An Python representation of an Intent can be built, and then converted into
    a Java representation using the buildIn() method to add context.
    """

    flags = {   'ACTIVITY_BROUGHT_TO_FRONT': 0x00400000,
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

        parser.add_argument("--action", help="action")
        parser.add_argument("--category", help="category")
        parser.add_argument("--component", help="component", nargs=2)
        parser.add_argument("--data-uri", help="data")
        parser.add_argument("--extra", action="append", default=[],
            dest="extras", nargs=3, help="extras")
        parser.add_argument("--flags", nargs='*', default=[], help="flags")
        parser.add_argument("--mimetype", help="mime")

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
        