# Quick Start Guide
## System Monitoring Tool

### 5-Minute Setup

#### Step 1: Install Python Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

If you encounter issues with audio libraries and don't need audio recording:
```bash
# Edit requirements.txt and comment out these lines:
# sounddevice==0.4.6
# scipy==1.11.4
# numpy==1.26.2

# Then install
pip install -r requirements.txt
```

#### Step 2: Configure Email Settings (2 minutes)

```bash
# Copy the example configuration
copy config.example.ini config.ini
```

Edit `config.ini` and set **minimum required** settings:

```ini
[Email]
smtp_server = smtp.gmail.com
smtp_port = 587
sender_email = YOUR_EMAIL@gmail.com
sender_password = YOUR_APP_PASSWORD
receiver_email = RECEIVER@example.com
```

**For Gmail Users** (RECOMMENDED):
1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2FA if not already enabled
3. Generate an app password for "Mail" + "Windows Computer"
4. Copy the 16-character password (no spaces) to config.ini

**For Other Email Providers**:
- **Outlook**: `smtp.office365.com` port `587`
- **Yahoo**: `smtp.mail.yahoo.com` port `587`

#### Step 3: Run (1 minute)

```bash
python system_monitor.py
```

You'll be asked for authorization:
1. Type `yes` when asked about authorization
2. Type `I ACCEPT` to confirm responsibility

Press **ESC** to stop monitoring.

---

### Common First-Time Issues

**Problem**: "config.ini not found"
```bash
copy config.example.ini config.ini
# Then edit config.ini with your settings
```

**Problem**: Email authentication fails
- Use **app-specific password**, NOT your regular password
- For Gmail: Must enable 2FA first
- Check if SMTP server and port are correct

**Problem**: "No module named 'win32clipboard'"
```bash
pip install pywin32
```

**Problem**: Audio recording fails
- Disable audio in config.ini: `enable_audio = false`
- Or install audio dependencies properly

---

### Testing Your Setup

#### Test 1: Check Configuration
```bash
python system_monitor.py
```
- Should ask for authorization
- Should NOT show "config.ini not found"

#### Test 2: Monitor for 1 Minute
1. Run the program
2. Type some text
3. Open a website
4. Copy/paste something
5. Wait 1 minute
6. Press ESC

#### Test 3: Check Outputs
```bash
# Check if directories were created
dir logs
dir screenshots

# Check if encryption key was generated
dir encryption.key

# Check logs
type monitor.log
```

---

### What Gets Monitored?

| Feature | What It Captures | Frequency |
|---------|-----------------|-----------|
| Keystrokes | Every key pressed | Real-time |
| Screenshots | Full screen images | Every 5 minutes |
| Clipboard | Copied text/data | Every minute |
| System Info | IP, OS, username | Once at start |
| Audio* | Microphone input | 30 seconds every minute |

*Audio disabled by default - requires explicit enable and consent

---

### Where Is Data Stored?

```
project/
├── logs/
│   ├── keystrokes.txt      ← Encrypted keyboard input
│   ├── clipboard.txt       ← Encrypted clipboard data
│   └── system_info.txt     ← Encrypted system details
│
├── screenshots/
│   └── screenshot_*.png    ← Screen captures
│
├── encryption.key          ← Encryption key (KEEP SAFE!)
└── monitor.log             ← Application log
```

**IMPORTANT**: All logs are encrypted by default!

---

### Quick Configuration Adjustments

#### Disable a Feature
Edit `config.ini`:
```ini
[Features]
enable_keylogging = false    # Disable keylogging
enable_screenshots = false   # Disable screenshots
enable_clipboard = false     # Disable clipboard
enable_audio = false         # Disable audio (default)
```

#### Change Email Frequency
```ini
[Intervals]
email_interval = 1800    # Send every 30 minutes (in seconds)
```

#### Change Screenshot Frequency
```ini
[Intervals]
screenshot_interval = 600    # Every 10 minutes
```

---

### Building Executable (Optional)

If you want a standalone `.exe` file:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller system_monitor.spec

# Find your exe at:
# dist/SystemMonitor.exe
```

---

### Security Reminders

✅ **DO**:
- Keep `config.ini` secure (it contains passwords)
- Keep `encryption.key` safe (needed to decrypt logs)
- Add both to `.gitignore` if using git
- Use app-specific passwords, not main passwords

❌ **DON'T**:
- Commit `config.ini` to GitHub
- Share your encryption key publicly
- Use your main email password
- Monitor systems without authorization

---

### Getting Help

1. **Read the full README.md** for detailed documentation
2. **Check monitor.log** for error messages
3. **Review Troubleshooting section** in README
4. **Verify all prerequisites** are installed
5. **Test with minimal configuration** first

---

### Legal Reminder

⚠️ **USE ONLY WITH AUTHORIZATION** ⚠️

This tool is for:
- Systems you own
- Authorized security testing
- Educational purposes
- With proper consent

Unauthorized use is ILLEGAL!

---

### Next Steps

Once everything works:

1. **Adjust intervals** in config.ini to your needs
2. **Test email reports** are being received
3. **Verify encryption** is working
4. **Set up auto-cleanup** to manage disk space
5. **Review logs regularly** for your use case

---

### Support

- **Documentation**: See README.md
- **Configuration**: See config.example.ini
- **Legal Questions**: Consult an attorney
- **Technical Issues**: Check monitor.log first

---

**You're ready to go! Remember: Use responsibly and legally.**
