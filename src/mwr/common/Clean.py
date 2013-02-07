
from mwr.cinnibar.reflection.types import ReflectedType


def clean(__reflector):
    """
    Clean the cache of all imported files
    """

    context = __reflector.resolve('com.mwr.droidhg.Agent').getContext()
    directory = context.getCacheDir().listFiles()
    i = 0
    for f in directory:
        if f.toString().endswith((".apk", ".dex")):
            f.delete()
            i+=1
    
    return i
