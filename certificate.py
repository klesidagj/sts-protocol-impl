from cryptography.hazmat.primitives import serialization

class Certificate:
    """Represents a certificate containing a public key, user name, and CA's signature."""

    def __init__(self, public_key, name, ca_signature):
        self.public_key = public_key
        self.name = name
        self.ca_signature = ca_signature

    def public_key_bytes(self):
        """Return the public key in bytes format."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def get_data_for_signature(self):
        """Return the data (public key + name) to be signed by the CA."""
        return self.public_key_bytes() + self.name.encode('utf-8')