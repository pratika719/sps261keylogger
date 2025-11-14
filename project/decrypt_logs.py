"""
Log Decryption Utility
Decrypts encrypted log files created by the System Monitoring Tool

Usage:
    python decrypt_logs.py [options]

Options:
    --key-file PATH       Path to encryption key file (default: encryption.key)
    --log-file PATH       Path to encrypted log file to decrypt
    --log-dir PATH        Path to directory containing log files (default: logs/)
    --output-dir PATH     Path to save decrypted files (default: decrypted/)
    --display            Display decrypted content in terminal (no save)
"""

import os
import sys
import argparse
from pathlib import Path
from cryptography.fernet import Fernet


class LogDecryptor:
    """Utility class for decrypting monitoring logs"""

    def __init__(self, key_file='encryption.key'):
        """
        Initialize decryptor with encryption key

        Args:
            key_file: Path to encryption key file
        """
        self.key_file = key_file
        self.cipher = None
        self._load_key()

    def _load_key(self):
        """Load encryption key from file"""
        try:
            if not os.path.exists(self.key_file):
                print(f"ERROR: Key file '{self.key_file}' not found!")
                print("Make sure you have the encryption.key file from the monitoring system.")
                sys.exit(1)

            with open(self.key_file, 'rb') as f:
                key = f.read()

            self.cipher = Fernet(key)
            print(f"✓ Loaded encryption key from {self.key_file}")

        except Exception as e:
            print(f"ERROR loading encryption key: {e}")
            sys.exit(1)

    def decrypt_data(self, encrypted_data):
        """
        Decrypt a single piece of encrypted data

        Args:
            encrypted_data: Encrypted bytes

        Returns:
            str: Decrypted text
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_data)
            return decrypted.decode('utf-8')
        except Exception as e:
            return f"[DECRYPTION ERROR: {e}]"

    def decrypt_file(self, input_file, output_file=None, display=False):
        """
        Decrypt an entire log file

        Args:
            input_file: Path to encrypted log file
            output_file: Path to save decrypted content (optional)
            display: If True, print to console instead of saving

        Returns:
            bool: True if successful
        """
        try:
            if not os.path.exists(input_file):
                print(f"ERROR: File '{input_file}' not found!")
                return False

            print(f"\nDecrypting: {input_file}")

            with open(input_file, 'rb') as f:
                encrypted_content = f.read()

            # Handle multiple encrypted blocks (separated by newlines)
            decrypted_parts = []
            blocks = encrypted_content.split(b'\n')

            for block in blocks:
                if block.strip():  # Skip empty blocks
                    decrypted = self.decrypt_data(block)
                    decrypted_parts.append(decrypted)

            full_content = '\n'.join(decrypted_parts)

            if display:
                print("\n" + "="*70)
                print(f"DECRYPTED CONTENT: {os.path.basename(input_file)}")
                print("="*70)
                print(full_content)
                print("="*70 + "\n")
            else:
                if output_file:
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(full_content)
                    print(f"✓ Saved decrypted content to: {output_file}")

            return True

        except Exception as e:
            print(f"ERROR decrypting file: {e}")
            return False

    def decrypt_directory(self, log_dir='logs', output_dir='decrypted'):
        """
        Decrypt all log files in a directory

        Args:
            log_dir: Directory containing encrypted logs
            output_dir: Directory to save decrypted files

        Returns:
            int: Number of files successfully decrypted
        """
        if not os.path.exists(log_dir):
            print(f"ERROR: Directory '{log_dir}' not found!")
            return 0

        print(f"\nDecrypting all files in: {log_dir}")
        print(f"Output directory: {output_dir}")

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Find all .txt files
        log_files = list(Path(log_dir).glob('*.txt'))

        if not log_files:
            print("No .txt files found in directory.")
            return 0

        success_count = 0

        for log_file in log_files:
            input_path = str(log_file)
            output_path = os.path.join(
                output_dir,
                f"decrypted_{log_file.name}"
            )

            if self.decrypt_file(input_path, output_path):
                success_count += 1

        print(f"\n✓ Successfully decrypted {success_count}/{len(log_files)} files")
        return success_count


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description='Decrypt logs from System Monitoring Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Decrypt all logs in logs/ directory
  python decrypt_logs.py --log-dir logs --output-dir decrypted

  # Decrypt a single file and display
  python decrypt_logs.py --log-file logs/keystrokes.txt --display

  # Decrypt with custom key file
  python decrypt_logs.py --key-file my_key.key --log-dir logs

  # Decrypt single file and save
  python decrypt_logs.py --log-file logs/keystrokes.txt --output-file decrypted.txt
        """
    )

    parser.add_argument(
        '--key-file',
        default='encryption.key',
        help='Path to encryption key file (default: encryption.key)'
    )

    parser.add_argument(
        '--log-file',
        help='Path to specific encrypted log file to decrypt'
    )

    parser.add_argument(
        '--log-dir',
        default='logs',
        help='Directory containing log files (default: logs/)'
    )

    parser.add_argument(
        '--output-dir',
        default='decrypted',
        help='Directory for decrypted files (default: decrypted/)'
    )

    parser.add_argument(
        '--output-file',
        help='Output file for single file decryption'
    )

    parser.add_argument(
        '--display',
        action='store_true',
        help='Display decrypted content in terminal (no file save)'
    )

    args = parser.parse_args()

    print("="*70)
    print("LOG DECRYPTION UTILITY")
    print("="*70)

    # Initialize decryptor
    decryptor = LogDecryptor(args.key_file)

    # Decrypt single file or directory
    if args.log_file:
        # Single file mode
        output = args.output_file if not args.display else None
        decryptor.decrypt_file(args.log_file, output, args.display)
    else:
        # Directory mode
        if args.display:
            print("WARNING: --display flag ignored in directory mode")
            print("Use --log-file for single file display")

        decryptor.decrypt_directory(args.log_dir, args.output_dir)

    print("\n" + "="*70)
    print("DECRYPTION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
