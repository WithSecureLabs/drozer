from drozer.modules.common import loader

class Assets(loader.ClassLoader):
    """
    Utility methods for interacting with the Android Asset Manager.
    """

    def getAndroidManifest(self, package):
        """
        Extract the AndroidManifest.xml file from a package on the device, and
        recover it as an XML representation.
        """

        XmlAssetReader = self.loadClass("common/XmlAssetReader.apk", "XmlAssetReader")

        asset_manager = self.getAssetManager(package)
        xml = asset_manager.openXmlResourceParser("AndroidManifest.xml")

        return str(XmlAssetReader.read(xml))

    def getAssetManager(self, package):
        """
        Get a handle on the AssetManager for the specified package.
        """

        return self.getContext().createPackageContext(package, 0).getAssets()
        