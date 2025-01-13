from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class KeyExchange:
    """Handles ECDH key generation and shared secret computation with parameters."""

    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.shared_key = None

    def generate_keys(self):
        """Generate ECDH keys."""
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()

    def compute_shared_key(self, peer_public_key):
        """Compute shared key using peer's public key."""
        shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)
        self.shared_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data'
        ).derive(shared_secret)