from cryptography.hazmat.primitives import serialization
from certificate_authority import CertificateAuthority
from key_exchange import KeyExchange
from certificate import Certificate

class STSParticipant:
    """Represents a participant in the STS protocol."""

    def __init__(self, name, ca: CertificateAuthority):
        self.name = name
        self.key_exchange = KeyExchange()
        self.key_exchange.generate_keys()
        self.ca = ca
        # Issue a certificate containing this participant's public key and name
        self.certificate = self.ca.issue_certificate(self.key_exchange.public_key, self.name)

    def send_initial_message(self):
        """First message from Alice to Bob, containing the public key."""
        return {'public_key': self.key_exchange.public_key}

    def store_initial_message(self, message):
        """Bob processes Alice's initial message and stores her public key."""
        alice_public_key = message['public_key']
        # Save Alice's public key for later use in shared secret computation
        self.peer_public_key = alice_public_key

    def send_response_message(self):
        """Second message from Bob to Alice, containing Bob's public key and certificate."""
        return {
            'public_key': self.key_exchange.public_key,
            'certificate': self.certificate
        }

    def verify_response_message(self, message):
        """Alice verifies Bob's public key and certificate."""
        bob_public_key = message['public_key']
        bob_certificate = message['certificate']

        # Verify Bob's certificate
        if not self.ca.verify_certificate(bob_certificate):
            raise ValueError("Invalid certificate for Bob.")

        # Check that Bob's certificate public key matches the public key in the message
        if bob_certificate.public_key_bytes() != bob_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ):
            raise ValueError("Mismatch between certificate public key and message public key.")

        # Save Bob's public key for shared secret computation
        self.peer_public_key = bob_public_key

    def send_final_message(self):
        """Third message from Alice to Bob, containing Alice's certificate."""
        return {'certificate': self.certificate}

    def verify_final_message(self, message):
        """Bob verifies Alice's certificate in the final message."""
        alice_certificate = message['certificate']

        # Verify Alice's certificate
        if not self.ca.verify_certificate(alice_certificate):
            raise ValueError("Invalid certificate for Alice.")

        # Check that Alice's certificate public key matches the stored public key
        if alice_certificate.public_key_bytes() != self.peer_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ):
            raise ValueError("Mismatch between certificate public key and stored public key.")

    def compute_shared_secret(self):
        """Compute the shared secret using the verified public key of the peer."""
        self.key_exchange.compute_shared_key(self.peer_public_key)
        print(f"{self.name}'s derived shared key: {self.key_exchange.shared_key.hex()}")