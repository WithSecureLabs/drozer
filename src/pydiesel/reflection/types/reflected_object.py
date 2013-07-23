from functools import partial

from pydiesel.api.protobuf_pb2 import Message
from pydiesel.reflection.exceptions import ReflectionException
from pydiesel.reflection.types.reflected_type import ReflectedType

class ReflectedObject(ReflectedType):
    """
    A ReflectedType that represents a Java Object.
    """

    def __init__(self, ref, *args, **kwargs):
        ReflectedType.__init__(self, *args, **kwargs)

        self._ref = ref
        self._class = None
        self._field_names = set()
        self._not_field_names = set(['_ref', 'getField'])

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return object.__getattribute__(self, attr)

        if attr in self._field_names:
            return self._reflector.getProperty(self, attr)

        if attr not in self._not_field_names:
            try:
                return self._reflector.getProperty(self, attr)
            except ReflectionException:
                self._not_field_names.add(attr)

        return partial(self._invoker, attr)

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            object.__setattr__(self, attr, value)
            return

        if attr in self._field_names:
            return self._reflector.setProperty(self, attr, ReflectedType.fromNative(value, reflector=self._reflector))

        if attr not in self._not_field_names:
            try:
                return self._reflector.setProperty(self, attr, ReflectedType.fromNative(value, reflector=self._reflector))
            except ReflectionException:
                self._not_field_names.add(attr)

    def _has_property(self, attr):
        """
        Test if a name is a property of the underlying Java object.
        """
        
        return not isinstance(self.__getattr__(attr), partial)
    
    def _invoker(self, method_name, *args, **kwargs):
        """
        Invokes methods on the object, in the Java VM, proxying through the
        reflector's invoke() method.
        """

        result = self._reflector.invoke(self, method_name, *map(lambda arg: ReflectedType.fromNative(arg, reflector=self._reflector), args), **kwargs)

        return result

    def _pb(self):
        """
        Get an Argument representation of the Object, as defined in the drozer
        protocol.
        """

        argument = Message.Argument(type=Message.Argument.OBJECT)

        argument.object.reference = self._ref

        return argument

    def __str__(self):
        return "#<Object {}>".format(self._ref)
        