
import base64

from merc.lib.modules import Module
from merc.lib.reflect import Reflect

class ClassLoader(Module):

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["test"]

    def twos_comp(self, num):
        num = num & 0xff
        result = num
        if num > 127:
            result = num - 256
        print result,
        return result

    def execute(self, session, args):

        f = open("merc/modules/test/file.jar", "rb")
        classdata = f.read()
        f.close()

        r = Reflect(session)
        classloader = r.classload(base64.b64encode(classdata))

        cls = classloader.loadClass("ManifestReader")

        ctx = r.getctx()
        obj = r.construct(cls)
        codelist = obj.main(ctx, 'com.sec.android.app.servicemodeapp')
        for i in codelist:
            print "  ", i
