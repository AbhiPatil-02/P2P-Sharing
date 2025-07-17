# 🔒 SecureP2P - Secure Peer-to-Peer File Sharing & Chat  

A secure, decentralized file sharing and chat application with military-grade encryption, built in Python. Transfer files and messages directly between devices without intermediaries.

---

## 🌟 Key Features  

### 🛡️ Security First  
- **End-to-End Encryption** (AES-128 via Fernet)  
- **Secure Key Exchange** during handshake  
- **No Data Storage** - Nothing leaves your device unencrypted  

### ⚡ Blazing Fast Local Transfers  
- LAN-optimized transfers (10x faster than cloud services)  
- Multi-threaded architecture  
- Dynamic port selection (3000-9000 range)  

### 💻 Easy Local Sharing  
- Works without internet connection  
- Automatic neighbor discovery (mDNS)  
- QR code connection setup  

---

## 🚀 Getting Started  

### Prerequisites  
- Python 3.7+  
- pip package manager  

### Installation  
```bash
# Install required packages
pip install tk tkinterdnd2 sv_ttk pillow cryptography ttkthemes
