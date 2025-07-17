# 🔒 Secure P2P File Sharing & Chat: End-to-End Encrypted Communication

---

## 📖 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features That Stand Out](#-features-that-stand-out)
- [⚙️ Installation: Get Started in Minutes!](#️-installation-get-started-in-minutes)
- [🚀 Usage: Connect & Communicate!](#-usage-connect--communicate)
- [🔧 Configuration: Tailor It to Your Needs](#-configuration-tailor-it-to-your-needs)
- [📦 Dependencies: The Power Behind the Scenes](#-dependencies-the-power-behind-the-scenes)
- [🗂️ File Structure: An Organized Approach](#️-file-structure-an-organized-approach)
- [🤝 Contributing & Contact: Join the Journey!](#-contributing--contact-join-the-journey)


---

## 🌟 Overview

Tired of relying on central servers for your private communications and file transfers? This project empowers you with a **secure, direct, and truly private** Peer-to-Peer (P2P) file sharing and chat application, all built in Python!

Experience **end-to-end encryption** that keeps your conversations and files exclusively between you and your peers.

### Why Choose This?

-   **🔐 Unwavering Security**: Powered by robust Fernet encryption for every message and file.
-   **⚡ Blazing Efficiency**: Leverage multi-threaded transfers and smart, dynamic port management for seamless experiences.
-   **🧩 Elegant Modularity**: Designed with clear, separated components, making it a breeze to understand, maintain, and even extend.

### Key Capabilities at a Glance

✔ **True P2P File Sharing**: No intermediaries, no central servers – just direct, secure transfer.
✔ **Encrypted Real-time Chat**: Speak freely with confidence, knowing your conversations are private.
✔ **Cross-Platform Compatibility**: Whether you're on Windows or Linux, it just works!
✔ **Intuitive User Interface**: A friendly GUI, built with `tkinter`, makes secure communication accessible to everyone.

---

## ✨ Features That Stand Out

### Ironclad Security

-   **AES-128 Encryption**: Utilizing the powerful Fernet library for top-tier cryptographic protection.
-   **Secure Key Exchange**: A robust key exchange mechanism is established during the initial handshake, ensuring your communications are always confidential from the get-go.

### Peak Performance

-   **Multi-threaded Transfers**: Say goodbye to bottlenecks! Transfer multiple files simultaneously without a hitch.
-   **Automatic Port Selection**: No manual configuration needed. The application intelligently selects available ports (within the 3000-9000 range) to get you connected faster.

### Seamless Usability

-   **Intuitive Graphical Interface**: A user-friendly GUI provides clear visual feedback, including real-time transfer progress.
-   **Smart Error Handling**: Built-in retry logic helps overcome transient network issues, ensuring your transfers complete successfully.

---

## ⚙️ Installation: Get Started in Minutes!

### Prerequisites

Before you begin, ensure you have:

-   **Python 3.7+**: Download and install the latest Python version from [python.org](https://www.python.org/).
-   **`pip` Package Manager**: Usually comes bundled with Python.

### Step-by-Step Installation

1.  **Clone the Repository**:
    Open your terminal or command prompt and run:
    ```bash
    git clone [https://github.com/your-username/secure-p2p-file-sharing.git](https://github.com/your-username/secure-p2p-file-sharing.git)
    cd secure-p2p-file-sharing
    ```

2.  **Install Dependencies**:
    Navigate into the cloned directory and install all required packages. Remember, your `requirements.txt` is in the main project directory, but the Python script to run is within `src`.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The `requirements.txt` file will handle `cryptography`, `Pillow`, `ttkthemes`, and `sv-ttk` for you!*

---
### GUI Options

Upon launch, you'll be presented with a simple, clear interface:

-   🖥️ **Host a Connection**: Become the host, awaiting an incoming connection from a peer.
-   🔌 **Connect to Peer**: Initiate a connection by entering the IP address of the peer you wish to connect to.

### Core Functionality

-   📁 **Effortless File Sharing**: Simply drag and drop files onto the application window to send them, or receive files seamlessly from your connected peer.
-   💬 **Secure Encrypted Chat**: Engage in real-time, private conversations through the integrated chat sidebar.

---

## 🔧 Configuration: Tailor It to Your Needs

For advanced users or specific network setups, you can customize certain aspects by editing the `config.ini` file. This file will be created automatically upon first run or should be placed directly in your project's root directory.

*Further details on `config.ini` parameters will be provided within the file itself.*

---

## 📦 Dependencies: The Power Behind the Scenes

This project relies on the following robust Python libraries:

| Package        | Purpose                                                                |
| :------------- | :--------------------------------------------------------------------- |
| `cryptography` | Essential for all Fernet encryption operations.                        |
| `tkinter`      | The foundational framework for the intuitive graphical user interface. |
| `Pillow`       | Handles image processing, potentially for avatars or file previews.    |
| `ttkthemes`    | Enhances the `tkinter` UI with modern, appealing themes.               |
| `sv-ttk`       | Provides a sleek, modern "Sun Valley" theme for `tkinter` applications. |

All these dependencies will be automatically installed when you run `pip install -r requirements.txt`.

---

## 🗂️ File Structure: An Organized Approach

All core application files are neatly organized within the `src` directory. Other folders like `__pycache__` will be created automatically by Python during execution.
Got it! Here's the content you provided, formatted clearly and ready for you to paste directly into your README.md file.

Markdown

### GUI Options

Upon launch, you'll be presented with a simple, clear interface:

-   🖥️ **Host a Connection**: Become the host, awaiting an incoming connection from a peer.
-   🔌 **Connect to Peer**: Initiate a connection by entering the IP address of the peer you wish to connect to.

### Core Functionality

-   📁 **Effortless File Sharing**: Simply drag and drop files onto the application window to send them, or receive files seamlessly from your connected peer.
-   💬 **Secure Encrypted Chat**: Engage in real-time, private conversations through the integrated chat sidebar.

---

## 🔧 Configuration: Tailor It to Your Needs

For advanced users or specific network setups, you can customize certain aspects by editing the `config.ini` file. This file will be created automatically upon first run or should be placed directly in your project's root directory.

*Further details on `config.ini` parameters will be provided within the file itself.*

---

## 📦 Dependencies: The Power Behind the Scenes

This project relies on the following robust Python libraries:

| Package        | Purpose                                                                |
| :------------- | :--------------------------------------------------------------------- |
| `cryptography` | Essential for all Fernet encryption operations.                        |
| `tkinter`      | The foundational framework for the intuitive graphical user interface. |
| `Pillow`       | Handles image processing, potentially for avatars or file previews.    |
| `ttkthemes`    | Enhances the `tkinter` UI with modern, appealing themes.               |
| `sv-ttk`       | Provides a sleek, modern "Sun Valley" theme for `tkinter` applications. |

All these dependencies will be automatically installed when you run `pip install -r requirements.txt`.

---

## 🗂️ File Structure: An Organized Approach

All core application files are neatly organized within the `src` directory. Other folders like `__pycache__` will be created automatically by Python during execution.

<pre>
secure-p2p-file-sharing/
├── src/
│   ├── Keep all .py files here                                    # Main application files
│   all required directories will be created automatically         # other file/folders

</pre>
---

## 🤝 Contributing & Contact: Join the Journey!

We'd love for you to contribute to making this project even better! Whether it's reporting bugs, suggesting new features, or submitting code, every contribution is highly valued.

### How to Contribute

1.  **Fork** the repository.
2.  **Create a new branch** for your feature or bug fix.
3.  **Make your changes** and ensure your code adheres to good practices.
4.  **Write clear commit messages**.
5.  **Submit a Pull Request** with a detailed description of your changes.

### Get in Touch!

Have questions, suggestions, or just want to chat about the project? Feel free to reach out!

📧 **Email**: patilrajakumar80@gmail.com


## 🚀 Usage: Connect & Communicate!

Once installed, launching and using the application is straightforward.

### Starting the Application

From your project's root directory, run:
```bash
python src/main.py
