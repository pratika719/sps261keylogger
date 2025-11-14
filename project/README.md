# System Monitoring Tool

## LEGAL DISCLAIMER

**READ THIS CAREFULLY BEFORE USE**

This tool is designed EXCLUSIVELY for:
- ✅ Authorized security testing with written permission
- ✅ Educational purposes in controlled environments
- ✅ Parental monitoring with proper legal authority
- ✅ Corporate IT monitoring with employee consent
- ✅ Security research on systems you own

**UNAUTHORIZED USE IS ILLEGAL** and may violate:
- Computer Fraud and Abuse Act (CFAA)
- Electronic Communications Privacy Act (ECPA)
- State and local privacy laws
- Workplace privacy regulations

**By using this tool, you accept full legal responsibility for your actions.**

---

## Overview

A comprehensive system monitoring application for authorized security testing and educational purposes. This tool demonstrates various system monitoring techniques including keystroke logging, screenshot capture, clipboard monitoring, and automated reporting.

### Features

- **Keystroke Logging**: Captures keyboard input with timestamps and encryption
- **Screenshot Capture**: Periodic screen captures at configurable intervals
- **Clipboard Monitoring**: Tracks clipboard content changes
- **System Information Collection**: Gathers IP addresses, hostname, OS details
- **Audio Recording**: Optional audio capture with legal warnings
- **Encrypted Data Storage**: All logs encrypted using Fernet encryption
- **Automated Email Reports**: Scheduled email delivery of monitoring data
- **Multi-Process Architecture**: Concurrent monitoring tasks
- **Graceful Shutdown**: Clean process termination
- **Authorization Checks**: Requires explicit user consent before starting

---

## Installation

### Prerequisites

- **Python 3.8+** (Python 3.11 recommended)
- **Windows OS** (due to win32clipboard dependency)
- **Administrator privileges** (for some monitoring features)

### Step 1: Clone/Download

```bash
cd C:\Users\prati\OneDrive\Desktop\pratik\keyslog\project
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you don't need audio recording, you can comment out the audio-related packages in `requirements.txt`:
```
# sounddevice==0.4.6
# scipy==1.11.4
# numpy==1.26.2
```

### Step 3: Configure

1. Copy the example configuration:
```bash
copy config.example.ini config.ini
```

2. Edit `config.ini` with your settings:

```ini
[Email]
smtp_server = smtp.gmail.com
smtp_port = 587
sender_email = your_email@gmail.com
sender_password = your_app_password  # Use app-specific password!
receiver_email = reports@example.com

[Intervals]
email_interval = 3600        # Send reports every hour
screenshot_interval = 300    # Screenshot every 5 minutes
clipboard_interval = 60      # Check clipboard every minute
keystroke_buffer = 10        # Write keystrokes after 10 keys

[Features]
enable_keylogging = true
enable_screenshots = true
enable_clipboard = true
enable_audio = false         # IMPORTANT: Requires additional legal compliance
enable_system_info = true

[Security]
encrypt_logs = true
auto_cleanup = true
max_log_age_days = 7
```

### Gmail Setup (Recommended)

For Gmail users:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App-Specific Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated password to `config.ini`

**Never use your regular Gmail password!**

---

## Usage

### Running the Application

```bash
python system_monitor.py
```

### Authorization Process

On startup, you'll see:

```
==================================================================
SYSTEM MONITORING TOOL - AUTHORIZATION REQUIRED
==================================================================

LEGAL WARNING:
This tool captures keystrokes, screenshots, clipboard data, and
other sensitive information. Use ONLY on systems you own or have
explicit written authorization to monitor.

...

Do you have proper authorization to monitor this system? (yes/no):
```

You must type `yes` and then `I ACCEPT` to proceed.

### Stopping the Monitoring

Press **ESC** key to initiate graceful shutdown. The tool will:
1. Stop all monitoring processes
2. Save any buffered data
3. Send a final email report
4. Clean up resources

### Monitoring Output

While running, the tool displays:
```
======================================================================
MONITORING ACTIVE
======================================================================
Press ESC to stop monitoring
Logs are being saved and encrypted
Email reports will be sent every 3600 seconds
======================================================================
```

---

## Building Executable

To create a standalone Windows executable:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build

```bash
pyinstaller system_monitor.spec
```

This creates `dist/SystemMonitor.exe` - a standalone executable with all dependencies bundled.

### Step 3: Distribution

Copy these files together:
```
SystemMonitor.exe
config.example.ini  (rename to config.ini and configure)
```

**Optional**: To hide the console window, edit `system_monitor.spec`:
```python
console=False,  # Change from True to False
```

---

## File Structure

```
project/
├── system_monitor.py          # Main application
├── keylogger.py               # Original basic keylogger (deprecated)
├── config.ini                 # Your configuration (DO NOT COMMIT)
├── config.example.ini         # Example configuration template
├── requirements.txt           # Python dependencies
├── system_monitor.spec        # PyInstaller specification
├── README.md                  # This file
├── encryption.key             # Generated encryption key (DO NOT COMMIT)
├── monitor.log                # Application log file
│
├── logs/                      # Encrypted log files
│   ├── keystrokes.txt        # Keystroke logs
│   ├── clipboard.txt         # Clipboard logs
│   └── system_info.txt       # System information
│
├── screenshots/               # Screenshot captures
│   └── screenshot_*.png
│
└── audio/                     # Audio recordings (if enabled)
    └── audio_*.wav
```

---

## Configuration Reference

### Email Settings

| Setting | Description | Example |
|---------|-------------|---------|
| `smtp_server` | SMTP server address | `smtp.gmail.com` |
| `smtp_port` | SMTP port (usually 587 for TLS) | `587` |
| `sender_email` | Email to send from | `monitor@example.com` |
| `sender_password` | App-specific password | `abcd efgh ijkl mnop` |
| `receiver_email` | Email to receive reports | `admin@example.com` |

### Intervals (in seconds)

| Setting | Description | Default |
|---------|-------------|---------|
| `email_interval` | How often to send reports | `3600` (1 hour) |
| `screenshot_interval` | Time between screenshots | `300` (5 min) |
| `clipboard_interval` | Clipboard check frequency | `60` (1 min) |
| `audio_duration` | Audio recording length | `30` seconds |
| `keystroke_buffer` | Keys before writing to disk | `10` keys |

### Features (true/false)

| Feature | Description | Legal Considerations |
|---------|-------------|---------------------|
| `enable_keylogging` | Log keyboard input | ⚠️ Privacy laws apply |
| `enable_screenshots` | Capture screen images | ⚠️ Privacy laws apply |
| `enable_clipboard` | Monitor clipboard | ⚠️ Privacy laws apply |
| `enable_audio` | Record audio | ⚠️⚠️ Wiretapping laws apply! |
| `enable_system_info` | Collect system details | ✅ Generally safe |

### Security Settings

| Setting | Description | Recommended |
|---------|-------------|-------------|
| `encrypt_logs` | Encrypt all log files | `true` |
| `auto_cleanup` | Delete old files after emailing | `true` |
| `max_log_age_days` | Days to keep old files | `7` |

---

## Security Considerations

### Encryption

- All sensitive data is encrypted using **Fernet (symmetric encryption)**
- Encryption key stored in `encryption.key` file
- Key is automatically generated on first run
- **IMPORTANT**: Include encryption key in email reports for decryption

### Credential Security

**DO NOT** hardcode credentials in the source code!

✅ **Good Practices**:
- Use `config.ini` (add to `.gitignore`)
- Use environment variables
- Use app-specific passwords (not your main password)
- Never commit `config.ini` or `encryption.key` to version control

❌ **Bad Practices**:
- Hardcoding passwords in Python files
- Using your main email password
- Committing credentials to GitHub
- Sharing encryption keys insecurely

### Log Management

- Logs are encrypted by default
- Old logs automatically cleaned after emailing (if `auto_cleanup = true`)
- Keep `encryption.key` secure - losing it means losing access to logs

---

## Legal and Ethical Use

### Authorized Use Cases

1. **Parental Control**
   - Monitoring minor children's computers
   - Must comply with local laws regarding parental rights

2. **Corporate IT**
   - Employee monitoring with proper notice and consent
   - Must comply with workplace privacy laws
   - Typically requires written policy and employee acknowledgment

3. **Security Research**
   - Testing on systems you own
   - Authorized penetration testing with client agreement
   - CTF competitions and educational labs

4. **Personal Use**
   - Monitoring your own devices
   - Testing security on systems you own

### Prohibited Use

❌ **NEVER use this tool to**:
- Monitor someone without their knowledge or consent
- Spy on spouses, partners, or roommates without consent
- Surveil employees without proper notice and legal basis
- Access systems you don't own or have authorization for
- Circumvent security measures
- Engage in stalking or harassment

### Legal Requirements

Before using this tool, ensure:

1. ✅ You have **written authorization** (for corporate/client systems)
2. ✅ You have **informed consent** (where required by law)
3. ✅ You comply with **all applicable laws**:
   - Computer Fraud and Abuse Act (USA)
   - Electronic Communications Privacy Act (USA)
   - General Data Protection Regulation (EU)
   - State/local privacy laws
   - Workplace monitoring laws
4. ✅ You have **consulted legal counsel** if unsure

**Penalties for unauthorized use can include**:
- Criminal charges and imprisonment
- Civil lawsuits and damages
- Termination of employment
- Professional license revocation

---

## Troubleshooting

### Common Issues

#### 1. `config.ini not found`

**Solution**: Copy `config.example.ini` to `config.ini` and configure it
```bash
copy config.example.ini config.ini
```

#### 2. Email authentication fails

**Causes**:
- Using regular password instead of app-specific password
- 2FA not enabled (required for Gmail app passwords)
- Incorrect SMTP settings

**Solutions**:
- Gmail: Generate app-specific password at https://myaccount.google.com/apppasswords
- Verify SMTP server and port settings
- Check firewall/antivirus blocking SMTP

#### 3. `ModuleNotFoundError: No module named 'win32clipboard'`

**Solution**: Install pywin32
```bash
pip install pywin32
```

#### 4. Audio recording fails

**Causes**:
- No audio input device
- Permissions issues
- sounddevice not installed

**Solutions**:
```bash
pip install sounddevice scipy numpy
```
- Check if microphone is connected and enabled
- Run as administrator

#### 5. Screenshots are black/blank

**Causes**:
- Multiple monitors with different DPI settings
- Protected content (DRM)
- Graphics driver issues

**Solutions**:
- Update graphics drivers
- Disable DRM in media players
- Check Windows display settings

#### 6. Executable won't build

**Solution**: Ensure all dependencies installed
```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --clean system_monitor.spec
```

---

## Decrypting Logs

If logs are encrypted (default), use this script to decrypt:

```python
from cryptography.fernet import Fernet

# Load the encryption key
with open('encryption.key', 'rb') as f:
    key = f.read()

cipher = Fernet(key)

# Decrypt a log file
with open('logs/keystrokes.txt', 'rb') as f:
    encrypted_data = f.read()

# Split on newlines if multiple encrypted blocks
for line in encrypted_data.split(b'\n'):
    if line:
        try:
            decrypted = cipher.decrypt(line)
            print(decrypted.decode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
```

---

## Advanced Configuration

### Custom SMTP Servers

**Outlook/Office 365**:
```ini
smtp_server = smtp.office365.com
smtp_port = 587
```

**Yahoo Mail**:
```ini
smtp_server = smtp.mail.yahoo.com
smtp_port = 587
```

**Custom Server**:
```ini
smtp_server = mail.yourcompany.com
smtp_port = 587
```

### Environment Variables

Instead of `config.ini`, you can use environment variables:

```python
# Add to system_monitor.py
import os

smtp_server = os.getenv('MONITOR_SMTP_SERVER', 'smtp.gmail.com')
sender_email = os.getenv('MONITOR_EMAIL')
sender_password = os.getenv('MONITOR_PASSWORD')
```

Set in Windows:
```cmd
set MONITOR_EMAIL=your_email@gmail.com
set MONITOR_PASSWORD=your_app_password
```

---

## Performance Considerations

### Resource Usage

| Feature | CPU Impact | Disk Impact | Network Impact |
|---------|-----------|-------------|----------------|
| Keylogging | Very Low | Low | None |
| Screenshots | Low-Medium | High | Medium (email) |
| Clipboard | Very Low | Low | None |
| Audio | Medium | Very High | High (email) |
| Email | Low | None | Medium |

### Optimization Tips

1. **Reduce screenshot frequency** if disk space is limited
2. **Disable audio recording** unless absolutely necessary
3. **Increase email interval** to reduce network usage
4. **Enable auto_cleanup** to manage disk space
5. **Use lower screenshot resolution** (modify code if needed)

---

## Development

### Running in Development Mode

```bash
# Install dev dependencies
pip install pytest black flake8

# Format code
black system_monitor.py

# Lint code
flake8 system_monitor.py

# Run tests (if you create them)
pytest tests/
```

### Project Structure for Development

```python
# Recommended modular structure
project/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── encryption.py       # Encryption utilities
│   ├── keylogger.py        # Keystroke logging
│   ├── screenshots.py      # Screenshot capture
│   ├── clipboard.py        # Clipboard monitoring
│   ├── audio.py            # Audio recording
│   ├── email_reporter.py   # Email functionality
│   └── system_info.py      # System information
├── tests/
│   ├── test_config.py
│   ├── test_encryption.py
│   └── ...
├── system_monitor.py       # Main entry point
└── requirements.txt
```

---

## Contributing

This is an educational project. If you want to improve it:

1. **Fork the repository**
2. **Create a feature branch**
3. **Add proper documentation**
4. **Include tests**
5. **Submit a pull request**

**Important**: All contributions must:
- Include legal disclaimers
- Emphasize ethical use
- Follow security best practices
- Not add features designed for evasion or stealth

---

## Educational Resources

### Learn More About:

- **Computer Security**: https://www.cybrary.it/
- **Ethical Hacking**: https://www.offensive-security.com/
- **Python Security**: https://realpython.com/python-security/
- **Cryptography**: https://cryptography.io/en/latest/
- **Legal Issues**: Consult your local attorney

### Related Topics

- Intrusion Detection Systems (IDS)
- Security Information and Event Management (SIEM)
- Endpoint Detection and Response (EDR)
- Data Loss Prevention (DLP)
- Insider Threat Detection

---

## Changelog

### Version 1.0.0 (2025)
- Initial release
- Keystroke logging with encryption
- Screenshot capture
- Clipboard monitoring
- Audio recording (optional)
- Automated email reporting
- Multi-process architecture
- Configuration management
- Authorization checks
- Graceful shutdown

---

## License

This project is provided for **educational and authorized testing purposes only**.

**NO WARRANTY**: This software is provided "as is" without warranty of any kind.

**DISCLAIMER**: The authors and contributors are not responsible for any misuse of this tool. You are solely responsible for ensuring your use complies with all applicable laws.

---

## Support

For issues, questions, or contributions:

1. **Check this README** first
2. **Review the troubleshooting section**
3. **Check the logs** (`monitor.log`)
4. **Consult legal counsel** for legal questions
5. **Open an issue** on GitHub (for technical issues only)

---

## Acknowledgments

Built with:
- [pynput](https://github.com/moses-palmer/pynput) - Keyboard/mouse monitoring
- [Pillow](https://python-pillow.org/) - Image processing
- [cryptography](https://cryptography.io/) - Encryption
- [PyInstaller](https://www.pyinstaller.org/) - Executable creation

---

## Final Warning

⚠️ **THINK BEFORE YOU ACT** ⚠️

Monitoring someone without authorization is:
- **Illegal**
- **Unethical**
- **Harmful**
- **Traceable**

This tool is designed to teach security concepts in authorized contexts. Use it responsibly and legally.

**When in doubt, don't do it. Get proper authorization first.**

---

**Stay legal. Stay ethical. Stay safe.**
