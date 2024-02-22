import OpenSSL
import unittest

from mwr.droidhg.ssl.ca import CA, NoKeyMaterialError

class CATestCase(unittest.TestCase):

    def testItShouldCreateACA(self):
        ca = CA()
        
        assert ca.create_ca()
    
    def testItShouldGetTheCACertificate(self):
        ca = CA()
        ca.create_ca()
        
        assert isinstance(ca.ca_cert, OpenSSL.crypto.X509)
    
    def testItShouldGetTheCAPrivateKey(self):
        ca = CA()
        ca.create_ca()
        
        assert isinstance(ca.ca_key, OpenSSL.crypto.PKey)
    
    def testTheCAKeyMaterialShouldBeValid(self):
        ca = CA()
        ca.create_ca()
        
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
        ctx.use_privatekey(ca.ca_key)
        ctx.use_certificate(ca.ca_cert)
        
        try:
            ctx.check_privatekey()
        except OpenSSL.SSL.Error:
            assert False, "key does not match certificate"
        except:
            pass
    
    def testItShouldNotHaveACAByDefault(self):
        ca = CA()
        
        assert not ca.has_ca()
    
    def testItShouldHaveACAAfterCreation(self):
        ca = CA()
        ca.create_ca()
        
        assert ca.has_ca()
        
    def testItShouldLoadACA(self):
        old_ca = CA()
        old_ca.create_ca()
        
        key_pem = CA.pkey_to_pem(old_ca.ca_key)
        cert_pem = CA.certificate_to_pem(old_ca.ca_cert)
        
        ca = CA()
        assert ca.load(key_pem, cert_pem)
    
    def testItShouldHaveACAAfterLoading(self):
        old_ca = CA()
        old_ca.create_ca()
        
        key_pem = CA.pkey_to_pem(old_ca.ca_key)
        cert_pem = CA.certificate_to_pem(old_ca.ca_cert)
        
        ca = CA()
        ca.load(key_pem, cert_pem)
        
        assert ca.has_ca()
    
    def testItShouldNotLoadACAFromInvalidKeyMaterial(self):
        old_ca = CA()
        old_ca.create_ca()
        
        key_pem = CA.pkey_to_pem(old_ca.ca_key)
        
        old_ca.create_ca()
        
        cert_pem = CA.certificate_to_pem(old_ca.ca_cert)
        
        ca = CA()
        assert not ca.load(key_pem, cert_pem)
        assert not ca.has_ca()
    
    def testItShouldCreateACertificate(self):
        ca = CA()
        ca.create_ca()
        
        key, certificate = ca.create_certificate()
        
        assert isinstance(key, OpenSSL.crypto.PKey)
        assert isinstance(certificate, OpenSSL.crypto.X509)
    
    def testItShouldNotCreateACertificateWithoutACA(self):
        ca = CA()
        
        try:
            ca.create_certificate()
            
            assert False, "expected NoKeyMaterialError"
        except NoKeyMaterialError:
            pass
        except:
            assert False, "expected NoKeyMaterialError"
    
    def testTheCertificateKeyMaterialShouldBeValid(self):
        ca = CA()
        ca.create_ca()
        
        key, certificate = ca.create_certificate()
        
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
        ctx.use_privatekey(key)
        ctx.use_certificate(certificate)
        
        try:
            ctx.check_privatekey()
        except OpenSSL.SSL.Error:
            assert False, "key does not match certificate"
        except:
            pass
    
    def testItShouldSerializeAPrivateKeyToPEM(self):
        ca = CA()
        ca.create_ca()
        
        assert CA.pkey_to_pem(ca.ca_key).find("PRIVATE KEY") >= 0
    
    def testItShouldSerializeACertificateToPEM(self):
        ca = CA()
        ca.create_ca()
        
        assert CA.certificate_to_pem(ca.ca_cert).find("CERTIFICATE") >= 0
    
def CATestSuite():
    suite = unittest.TestSuite()

    suite.addTest(CATestCase("testItShouldCreateACA"))
    suite.addTest(CATestCase("testItShouldGetTheCACertificate"))
    suite.addTest(CATestCase("testItShouldGetTheCAPrivateKey"))
    suite.addTest(CATestCase("testTheCAKeyMaterialShouldBeValid"))
    suite.addTest(CATestCase("testItShouldNotHaveACAByDefault"))
    suite.addTest(CATestCase("testItShouldHaveACAAfterCreation"))
    suite.addTest(CATestCase("testItShouldLoadACA"))
    suite.addTest(CATestCase("testItShouldHaveACAAfterLoading"))
    suite.addTest(CATestCase("testItShouldNotLoadACAFromInvalidKeyMaterial"))
    suite.addTest(CATestCase("testItShouldCreateACertificate"))
    suite.addTest(CATestCase("testItShouldNotCreateACertificateWithoutACA"))
    suite.addTest(CATestCase("testTheCertificateKeyMaterialShouldBeValid"))
    suite.addTest(CATestCase("testItShouldSerializeAPrivateKeyToPEM"))
    suite.addTest(CATestCase("testItShouldSerializeACertificateToPEM"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(CATestSuite())
    