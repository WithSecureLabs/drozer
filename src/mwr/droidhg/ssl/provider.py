import os
import OpenSSL
import random
import shlex
import string

from mwr.common import fs, system

from mwr.droidhg.configuration import Configuration
from mwr.droidhg.ssl import ca

class Provider(object):
    
    def __init__(self):
        self.authority = ca.CA()
    
    def ca_certificate_path(self):
        """
        Get the path to the CA Certificate.
        """
        
        return self.__certificate_path("mercury-ca")
    
    def ca_path(self):
        """
        Get the path to the CA Key Material, as defined by the configuration file.
        """
        
        ca_path = Configuration.get("ssl", "ca_path")
        
        if ca_path == None:
            ca_path = os.path.abspath(os.curdir)
        
        return ca_path

    def certificate_exists(self):
        """
        True, if the CA certificate file exists, and can be read.
        """
        
        return os.path.exists(self.ca_certificate_path())
    
    def create_keypair(self, cn):
        """
        Create a key/certificate pair, signed with the CA.
        """
        
        self.__load_key_material()
        
        key, certificate = self.authority.create_certificate(cn)
        
        fs.write(self.__certificate_path(cn), ca.CA.certificate_to_pem(certificate))
        fs.write(self.__key_path(cn), ca.CA.pkey_to_pem(key))
        
        return (key, certificate)
    
    def digest(self, certificate):
        """
        Calculate the SHA-1 digest of an X509 certificate.
        """
        
        return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, certificate).digest('sha1')
    
    def get_keypair(self, cn):
        """
        Retrieves a key pair, stored in the CA.
        """
        
        return (self.__key_path(cn), self.__certificate_path(cn))
        
    def key_exists(self):
        """
        True, if the CA key file exists, and can be read.
        """
        
        return os.path.exists(self.__ca_key_path())
    
    def key_material_exists(self):
        """
        True, if the CA Key Material exists.
        """
        
        return self.key_exists() and self.certificate_exists()
    
    def key_material_valid(self):
        """
        Tests the given Key Material, to determine if it is a valid key pair.
        """
        
        self.__load_key_material()
        
        return self.authority.verify_ca()
    
    def keypair_exists(self, cn):
        """
        True, if a keypair by the specified CN exists.
        """
        
        key, certificate = self.get_keypair(cn)
        
        return os.path.exists(key) and os.path.exists(certificate)
    
    def make_bks_key_store(self, cn, p12_path, export_password, store_password, key_password):
        """
        Prepare a BouncyCastle KeyStore from a PKCS12 bundle.
        """
        
        keytool = system.which('keytool') 
        argv = shlex.split(("%s " +
                            "-importkeystore "+
                            "-deststorepass %s "+
                            "-destkeypass %s " +
                            "-destkeystore %s " +
                            "-deststoretype BKS " + 
                            "-provider org.bouncycastle.jce.provider.BouncyCastleProvider " +
                            "-providerpath /usr/local/share/classpath/bcprov-ext-jdk15on-1.46.jar " +
                            "-srckeystore %s " +
                            "-srcstoretype PKCS12 " +
                            "-srcstorepass %s " +
                            "-alias mercury") % (keytool, store_password, key_password, self.__bks_path(cn), p12_path, export_password))
        
        if os.spawnvpe(os.P_WAIT, argv[0], argv, os.environ) == 0:
            return self.__bks_path(cn)
    
    def make_bks_trust_store(self):
        """
        Prepare a BouncyCastle TrustStore, for the CA.
        """
        
        keytool = system.which('keytool')
        argv = shlex.split(("%s " +
                            "-import " +
                            "-trustcacerts " +
                            "-alias mercuryCA " +
                            "-file %s " +
                            "-keystore %s " +
                            "-storetype BKS " +
                            "-storepass %s " +
                            "-provider org.bouncycastle.jce.provider.BouncyCastleProvider " +
                            "-providerpath /usr/local/share/classpath/bcprov-ext-jdk15on-1.46.jar") % (keytool, self.ca_certificate_path(), self.__bks_path('mercury-ca'), "mercury"))
        
        if os.spawnvpe(os.P_WAIT, argv[0], argv, os.environ) == 0:
            return self.__bks_path('mercury-ca')
        
    def make_pcks12(self, cn, key, cert, export_password=None):
        """
        Prepare a PKCS12 package, given a key and a certificate.
        """
        
        if export_password == None:
            export_password = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(12))
        
        pkcs12 = OpenSSL.crypto.PKCS12()
        pkcs12.set_friendlyname("mercury")
        pkcs12.set_ca_certificates([self.authority.ca_cert])
        pkcs12.set_certificate(cert)
        pkcs12.set_privatekey(key)
        
        fs.write(os.path.join(self.ca_path(), "%s.p12" % cn), pkcs12.export(export_password))
        
        return (os.path.join(self.ca_path(), "%s.p12" % cn), export_password)
        
    def provision(self, path):
        """
        Provision new CA Key Material.
        
        This will overwrite any existing CA.
        """
        
        self.authority.create_ca()
        
        Configuration.set("ssl", "ca_path", path)
        
        fs.write(self.ca_certificate_path(), ca.CA.certificate_to_pem(self.authority.ca_cert))
        fs.write(self.__ca_key_path(), ca.CA.pkey_to_pem(self.authority.ca_key))
        
        return True
    
    def trust(self, certificate, peer):
        """
        Add the certificate to the SSL Known Hosts in the Configuration file, so we will
        always trust this host in future.
        """
        
        Configuration.set("ssl-known-hosts", "%s|%d" % peer, self.digest(certificate))
    
    def trusted(self, certificate, peer):
        """
        Determine if the certificate/peer pair have been previously trusted.
        
         0 - Trusted
        -1 - Not Trusted
        -2 - Wrong Certificate
        """
        
        known_certificate = self.trusted_certificate_for(peer)
        
        if known_certificate == None:
            return -1
        elif known_certificate == self.digest(certificate):
            return 0
        else:
            return -2
    
    def trusted_certificate_for(self, peer):
        """
        Fetches the trusted certificate for a peer.
        """
        
        return Configuration.get("ssl-known-hosts", "%s|%d" % peer)
    
    def __bks_path(self, cn):
        """
        Get the path to a BouncyCastle KeyStore file.
        """
        
        return os.path.join(self.ca_path(), "%s.bks" % cn)
        
    def __ca_key_path(self):
        """
        Get the path to the CA Key.
        """
        
        return self.__key_path("mercury-ca")
    
    def __certificate_path(self, cn):
        """
        Get the path to a certificate file.
        """
        
        return os.path.join(self.ca_path(), "%s.crt" % cn)
    
    def __key_path(self, cn):
        """
        Get the path to a key file.
        """
        
        return os.path.join(self.ca_path(), "%s.key" % cn)
        
    def __load_key_material(self):
        """
        Loads Key Material into the authority, from disk.
        """
        
        if not self.authority.has_ca() and self.key_material_exists():
            self.authority.load(fs.read(self.__ca_key_path()), fs.read(self.ca_certificate_path()))
            