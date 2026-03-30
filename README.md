# QuantumSecureMessagingApp
Quantum secure ephemeral messaging system with encryption, auto-deleting messages, and Random Forest based prediction for message lifetime and privacy enhancement.
PROJECT TITLE:
Quantum + ML Based Ephemeral Secure Messaging Bot

PROJECT IDEA:
This project is a secure messaging Telegram bot where messages automatically disappear after being read. It combines quantum-inspired key generation, basic encryption, and machine learning to control how long a message is visible.

WHAT IS EPHEMERAL?
Ephemeral means something that lasts for a very short time. In this project, messages exist only briefly and are automatically deleted.

PROJECT DESCRIPTION:
This system provides a zero-trace secure communication method. A sender creates a secure channel using a username, sends a message, and the message is stored temporarily in RAM. The receiver retrieves it once, views it, and it gets deleted automatically. No message is permanently stored anywhere.

Quantum key generation is simulated using Qiskit. The key is used to encrypt and decrypt the message. A machine learning model (Random Forest Regressor) dynamically decides how long the message should be visible based on message complexity.

HOW QUANTUM IS USED:
Quantum circuits are used to generate random keys using superposition. This improves randomness compared to classical methods and enhances security in encryption.

HOW ML IS USED:
A Random Forest Regressor is trained using sample data to predict how long a message should be displayed.

Features used:
- Message length
- Number of words
- Average word length
- Special characters count

Based on these, the model predicts display time (5–30 seconds).

MODEL DETAILS:
Model Used: RandomForestRegressor

Training Data:
Input Features:
[10, 2, 4, 0]
[25, 5, 4.5, 1]
[50, 10, 5, 2]
[75, 15, 5.5, 3]
[100, 20, 6, 5]

Output (time in seconds):
[5, 8, 12, 18, 25]

The model learns patterns and predicts display duration dynamically.

ENCRYPTION METHOD:
A simple XOR encryption is used with a quantum-generated key. The same key is used for decryption.

FEATURES:
- Quantum-based key generation
- ML-based adaptive message timing
- One-time message retrieval
- Auto deletion of messages
- RAM-only storage (no database)
- Zero trace communication

WORKFLOW:
1. User sends /create @username
2. Bot opens secure channel
3. Sender sends message
4. Message gets encrypted using quantum key
5. Stored temporarily in RAM
6. Receiver uses /retrieve
7. Message is decrypted and shown
8. ML decides display time
9. Message auto-deletes after viewing
10. Data is removed permanently

ADVANTAGES:
- No message storage → high privacy
- Quantum randomness → stronger keys
- ML optimization → smart timing
- Auto deletion → no trace

LIMITATIONS:
- Quantum is simulated (not real hardware)
- Basic XOR encryption (can be improved)
- Requires Telegram username

SAMPLE TEST MESSAGE:
Hello, this is a highly confidential message containing sensitive project details, login credentials, and encryption keys. Please read carefully and do not share this information with anyone else. This message will self-destruct shortly after viewing to ensure complete security and privacy.
