
# Station-to-Station (STS) Protocol Implementation

This project implements a simplified version of the Station-to-Station (STS) protocol for secure, authenticated key exchange between two participants (e.g., Alice and Bob). The project is structured into multiple classes to handle different components of the protocol, including certificate management, key exchange, and participant interactions.

---

## **Overview**

The protocol uses:
- **Elliptic Curve Diffie-Hellman (ECDH)** for key exchange.
- **Certificates** issued by a Certificate Authority (CA) to authenticate public keys and ensure integrity.
- A **three-message workflow** where Alice and Bob exchange certificates and verify each other’s public keys to prevent man-in-the-middle attacks.

---

## **File Structure**
```
certificate.py: Defines the Certificate class, representing a digital certificate that includes a user’s public key and the CA’s signature.
certificate_authority.py: Defines the CertificateAuthority class, which issues and verifies certificates.
key_exchange.py: Defines the KeyExchange class, which handles ECDH key generation and shared secret computation.
participant.py: Defines the STSParticipant class, which represents a protocol participant (Alice or Bob) and manages the STS protocol steps.
main.py: Defines the protocol workflow between Alice and Bob.
```

---

## **Class Descriptions**

### **Certificate Class**
Represents a digital certificate that contains a user’s public key, their name, and a CA’s signature.

- **Attributes:**
  - `public_key`: The public key of the participant (ECDH public key).
  - `name`: The name of the participant (e.g., “Alice” or “Bob”).
  - `ca_signature`: The CA’s digital signature over the participant’s public key and name.
- **Methods:**
  - `public_key_bytes()`: Serializes the public key to bytes for inclusion in the certificate. It uses PEM encoding and SubjectPublicKeyInfo format.
  - `get_data_for_signature()`: Returns a byte sequence combining the public key and name. This data is what the CA signs to create a certificate.

### **CertificateAuthority Class**
Simulates a Certificate Authority (CA) that issues and verifies certificates.

- **Attributes:**
  - `private_key`: The CA’s private RSA key used for signing certificates.
  - `public_key`: The CA’s public RSA key used to verify certificates.
- **Methods:**
  - `issue_certificate(user_public_key, user_name)`: Issues a certificate by signing the user’s public key and name with the CA’s private key.
  - `verify_certificate(certificate)`: Verifies the CA’s signature on a given certificate.

### **KeyExchange Class**
Manages the generation of Elliptic Curve Diffie-Hellman (ECDH) keys and computation of a shared secret between two participants.

- **Attributes:**
  - `private_key`: The participant’s private ECDH key.
  - `public_key`: The participant’s public ECDH key.
  - `shared_key`: The computed shared secret derived from the participant’s private key and the peer’s public key.
- **Methods:**
  - `generate_keys()`: Generates a new ECDH key pair.
  - `compute_shared_key(peer_public_key)`: Computes a shared secret and derives a shared symmetric key using HKDF.

### **Participant Class**
Represents a participant in the STS protocol (e.g., Alice or Bob).

- **Attributes:**
  - `name`: The participant’s name (e.g., “Alice” or “Bob”).
  - `key_exchange`: An instance of KeyExchange.
  - `ca`: A reference to the CertificateAuthority.
  - `certificate`: The participant’s certificate.
- **Methods:**
  - `send_initial_message()`: Sends the participant’s public key in the first message.
  - `store_initial_message(message)`: Stores the public key from the initial message.
  - `send_response_message()`: Sends the participant’s public key and certificate in the second message.
  - `verify_response_message(message)`: Verifies the received certificate and public key.
  - `send_final_message()`: Sends the participant’s certificate in the final message.
  - `verify_final_message(message)`: Verifies the certificate received in the final message.
  - `compute_shared_secret(peer_public_key)`: Computes the shared secret based on the peer’s verified public key.

---

## **Workflow**

1. **Initialization:**
   - A CertificateAuthority (CA) is created.
   - Alice and Bob receive certificates issued by the CA.

2. **Step 1: Alice Sends Initial Message**
   - Alice sends her public key to Bob.
   - Bob stores Alice’s public key.

3. **Step 2: Bob Sends Response Message**
   - Bob sends his public key and certificate to Alice.
   - Alice verifies Bob’s certificate and public key.

4. **Step 3: Alice Sends Final Message**
   - Alice sends her certificate to Bob.
   - Bob verifies Alice’s certificate and public key.

5. **Key Exchange:**
   - Alice and Bob compute the shared secret using the verified public keys.

---

## **Usage**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sts-protocol.git
   cd sts-protocol
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the protocol:
   ```bash
   python main.py
   ```

---
