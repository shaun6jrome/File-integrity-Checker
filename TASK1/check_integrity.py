import os
import hashlib
import json
import datetime

# Log file path
log_file_path = "integrity_log.txt"

# Create log entry
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entries = [f"🕒 Check Time: {timestamp}\n"]

# Initialize variables for added, deleted, and modified files
added, deleted, modified = set(), set(), set()

if added:
    log_entries.append(f"🟢 Added files ({len(added)}):")
    for f in added:
        log_entries.append(f"  + {f}")
if deleted:
    log_entries.append(f"🔴 Deleted files ({len(deleted)}):")
    for f in deleted:
        log_entries.append(f"  - {f}")
if modified:
    log_entries.append(f"🟡 Modified files ({len(modified)}):")
    for f in modified:
        log_entries.append(f"  * {f}")
if not (added or deleted or modified):
    log_entries.append("✅ No changes detected.")

log_entries.append("-" * 40 + "\n")

# Write to log file
with open(log_file_path, 'a') as log_file:
    log_file.write("\n".join(log_entries))

print(f"\n📝 Changes logged to: {log_file_path}")
def calculate_file_hash(filepath, hash_algo='sha256'):
    hash_func = hashlib.new(hash_algo)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def check_integrity(directory, baseline_file='file_baseline.json'):
    # Load baseline hashes
    if not os.path.exists(baseline_file):
        print(f"Baseline file '{baseline_file}' not found. Create a baseline first.")
        return

    with open(baseline_file, 'r') as bf:
        baseline_data = json.load(bf)
    
    baseline_files = baseline_data.get('files', {})
    current_files = {}

    # Calculate current hashes
    for root, _, files in os.walk(directory):
        for fname in files:
            full_path = os.path.join(root, fname)
            try:
                current_files[full_path] = calculate_file_hash(full_path)
            except Exception as e:
                print(f"Error hashing file {full_path}: {e}")

    # Detect added, deleted, and modified files
    added = set(current_files) - set(baseline_files)
    deleted = set(baseline_files) - set(current_files)
    modified = {f for f in current_files if f in baseline_files and current_files[f] != baseline_files[f]}

    # Report results
    if added:
        print(f"\nAdded files ({len(added)}):")
        for f in added:
            print(f"  + {f}")
    if deleted:
        print(f"\nDeleted files ({len(deleted)}):")
        for f in deleted:
            print(f"  - {os.path.abspath(f)}")
    if modified:
        print(f"\nModified files ({len(modified)}):")
        for f in modified:
            print(f"  * {f}")

    if not (added or deleted or modified):
        print("\nNo changes detected. All files are intact.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python check_integrity.py <directory_to_check>")
        sys.exit(1)
    
    directory_to_check = sys.argv[1]
    check_integrity(directory_to_check)

