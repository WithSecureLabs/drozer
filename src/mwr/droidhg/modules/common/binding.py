from mwr.droidhg.modules.common import loader

class ServiceBinding(loader.ClassLoader):
    
    class ServiceBindingProxy(object):
        
        def __init__(self, context, package, component):
            self.context = context
            self.package = package
            self.component = component
            
            self.binder = None
        
        def getData(self):
            return self.binder.getData()
        
        def obtain_binder(self):
            if self.binder == None:
                ServiceBinder = self.context.loadClass("common/ServiceBinder.apk", "ServiceBinder")
                
                self.binder = self.context.new(ServiceBinder)
                
            return self.binder
            
        def obtain_message(self, msg, bundle):
            Message = self.context.klass("android.os.Message")
            
            return Message.obtain(None, msg, bundle)
        
        def send_message(self, msg, bundle):
            binder = self.obtain_binder()
            message = self.obtain_message(msg, bundle)
            
            return binder.execute(self.context.getContext(), self.package, self.component, message)
    
    def getBinding(self, package, component):
        return ServiceBinding.ServiceBindingProxy(self, package, component)
        