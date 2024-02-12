from drozer.modules.common import loader

class ZipFile(loader.ClassLoader):
    """
    Utility methods for interacting with zipped archive files.
    """

    def extractFromZip(self, target, source, destination):
        """
        Extract a file (target) from a zipped archive (source) and save it to
        the file system (destination).
        """

        ZipUtil = self.loadClass("common/ZipUtil.apk", "ZipUtil")

        return ZipUtil.unzip(target, source, destination)
