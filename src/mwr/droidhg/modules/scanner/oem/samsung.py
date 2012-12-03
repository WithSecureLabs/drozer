from mwr.droidhg.modules import common, Module

class Samsung(Module, common.VulnerabilityScanner):

    name = "Test for multiple Samsung content provider vulnerabilities"
    description = "Tests for multiple vulnerabilities in content providers exposed by Samsung OEM software."
    examples = ""
    author = ["Mike (@mwrlabs)", "Tyrone (@mwrlabs)"]
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["scanner", "oem"]

    vulnerabilities = "exploit.pilfer.oem.samsung."
    