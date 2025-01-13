from certificate_authority import CertificateAuthority
from participant import STSParticipant

def simulate_sts_protocol():
    # Initialize the Certificate Authority
    ca = CertificateAuthority()

    # Initialize participants Alice and Bob
    alice = STSParticipant("Alice", ca)
    bob = STSParticipant("Bob", ca)

    # Step 1: Alice sends her initial message (public key) to Bob
    alice_initial_message = alice.send_initial_message()
    bob.store_initial_message(alice_initial_message)

    # Step 2: Bob sends his response message (public key and certificate) to Alice
    bob_response_message = bob.send_response_message()
    alice.verify_response_message(bob_response_message)

    # Step 3: Alice sends her final message (certificate) to Bob
    alice_final_message = alice.send_final_message()
    bob.verify_final_message(alice_final_message)

    # Compute shared secrets after all messages are verified
    alice.compute_shared_secret()
    bob.compute_shared_secret()

if __name__ == "__main__":
    simulate_sts_protocol()