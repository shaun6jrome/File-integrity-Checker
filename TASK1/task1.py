import hashlib
import os
import json
from datetime import datetime
import argparse

class FileIntegrityChecker:
    def __init__(self, baseline_file="file_baseline.json"):
        self.baseline_file = baseline_file
        self.baseline_data = self.load_baseline()

    def calculate_hash(self, file_path, algorithm='sha256'):
        """Calculate the hash of a file using the specified algorithm."""
        try:
            hash_func = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except (IOError, PermissionError) as e:
            print(f"⚠️ Error reading file {file_path}: {e}")
            return None
        except Exception as e:
            print(f"⚠️ Unexpected error calculating hash for {file_path}: {e}")
            return None

    def load_baseline(self):
        """Load the baseline data from the JSON file."""
        try:
            if os.path.exists(self.baseline_file):
                with open(self.baseline_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Error loading baseline file: {e}")
            return {}

    def save_baseline(self):
        """Save the current baseline data to the JSON file."""
        try:
            with open(self.baseline_file, 'w') as f:
                json.dump(self.baseline_data, f, indent=4)
            print(f"✅ Baseline saved to {self.baseline_file}")
        except Exception as e:
            print(f"⚠️ Error saving baseline file: {e}")

    def create_baseline(self, directory):
        """Create a new baseline for all files in the specified directory."""
        try:
            if not os.path.isdir(directory):
                print(f"❌ Error: {directory} is not a valid directory")
                return False

            print(f"🔍 Creating new baseline for directory: {directory}")
            self.baseline_data = {
                'directory': os.path.abspath(directory),
                'timestamp': datetime.now().isoformat(),
                'files': {}
            }

            file_count = 0
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_hash = self.calculate_hash(file_path)
                        if file_hash:
                            relative_path = os.path.relpath(file_path, directory)
                            self.baseline_data['files'][relative_path] = {
                                'hash': file_hash,
                                'last_checked': datetime.now().isoformat()
                            }
                            file_count += 1
                    except Exception as e:
                        print(f"⚠️ Skipping file {file_path}: {e}")

            self.save_baseline()
            print(f"✅ Baseline created with {file_count} files")
            return True
        except Exception as e:
            print(f"❌ Failed to create baseline: {e}")
            return False

    def verify_integrity(self):
        """Verify the integrity of files against the baseline."""
        try:
            if not self.baseline_data or 'directory' not in self.baseline_data:
                print("❌ No baseline data available. Please create a baseline first.")
                return None

            directory = self.baseline_data['directory']
            if not os.path.isdir(directory):
                print(f"❌ Error: Baseline directory {directory} no longer exists")
                return None

            print(f"🔎 Verifying integrity against baseline for directory: {directory}")
            changed_files = []
            new_files = []
            missing_files = []

            # Check existing files in baseline
            for relative_path, file_data in self.baseline_data['files'].items():
                file_path = os.path.join(directory, relative_path)
                if not os.path.exists(file_path):
                    missing_files.append(relative_path)
                    continue

                current_hash = self.calculate_hash(file_path)
                if current_hash != file_data['hash']:
                    changed_files.append(relative_path)

            # Check for new files not in baseline
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    if relative_path not in self.baseline_data['files']:
                        new_files.append(relative_path)

            # Update last checked time
            for relative_path in self.baseline_data['files']:
                self.baseline_data['files'][relative_path]['last_checked'] = datetime.now().isoformat()
            self.save_baseline()

            # Print results
            if not (changed_files or new_files or missing_files):
                print("✅ All files match the baseline. No changes detected.")
            else:
                if changed_files:
                    print("\n🔄 Changed files:")
                    for file in changed_files:
                        print(f" - {file}")
                if new_files:
                    print("\n🆕 New files (not in baseline):")
                    for file in new_files:
                        print(f" - {file}")
                if missing_files:
                    print("\n❌ Missing files (in baseline but not found):")
                    for file in missing_files:
                        print(f" - {file}")

            return {
                'changed': changed_files,
                'new': new_files,
                'missing': missing_files
            }
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(
        description="📂 File Integrity Checker - Monitor changes in files by comparing hash values",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True, title='commands')

    # Create baseline command
    create_parser = subparsers.add_parser(
        'create',
        help='Create a new baseline of file hashes'
    )
    create_parser.add_argument(
        'directory',
        help='Directory to create baseline for'
    )

    # Verify command
    verify_parser = subparsers.add_parser(
        'verify',
        help='Verify files against the baseline'
    )

    args = parser.parse_args()

    checker = FileIntegrityChecker()

    if args.command == 'create':
        checker.create_baseline(args.directory)
    elif args.command == 'verify':
        checker.verify_integrity()

if __name__ == "__main__":
    main()


    