from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
from certificate import Certificate


class CertificateAuthority:
    """Simulates a CA that issues and verifies certificates."""

    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def issue_certificate(self, user_public_key, user_name):
        """Sign and issue a certificate for the user, containing their public key."""
        # The data to sign includes the public key and the user name
        data = user_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ) + user_name.encode('utf-8')

        signature = self.private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Return a certificate containing the user's public key, name, and CA's signature
        return Certificate(user_public_key, user_name, signature)

    def verify_certificate(self, certificate):
        """Verify the certificate signature using the CA's public key."""
        data = certificate.get_data_for_signature()
        try:
            self.public_key.verify(
                certificate.ca_signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            print("Certificate verification failed.")
            return False