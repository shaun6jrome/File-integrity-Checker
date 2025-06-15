# File-integrity-Checker

*COMPANY NAME* : CODTECH IT SOLUTIONS


*NAME* : SHAUN JEROME


*INTERN ID* : CT04DM953


*DOMAIN* : Cyber Security & Ethical Hacking


*DURATION* : 4 WEEKS


*MENTOR* : NEELA SANTHOSH



*DESCRIPTION* 
Introduction

In the field of cybersecurity and system maintenance, ensuring that sensitive or critical files remain unaltered is a fundamental requirement. Unauthorized changes to system files, configuration files, scripts, or application assets can be signs of malware infection, unauthorized access, or accidental modification. This task is focused on building a File Integrity Checker, a tool that ensures the consistency and trustworthiness of files in a directory by monitoring changes based on cryptographic hashes.

A File Integrity Checker is a proactive security mechanism. It helps detect alterations in files by maintaining a record of their original state and comparing them against the current state during subsequent verifications. This approach is widely used in intrusion detection systems (IDS), forensic analysis, backup integrity validation, and compliance auditing.

⸻

Objective of the Task

The primary objective of this task is to create a Python-based tool that can monitor file changes in a specified directory. This tool must utilize a cryptographic hash function to generate unique digital fingerprints of files. These fingerprints, or hashes, are then stored as a baseline in a structured format. Over time, the tool can be re-run to verify if any files have been changed, deleted, or added by comparing current hashes to the stored baseline.

This task involves applying key concepts in:
	•	Cryptographic hashing
	•	File system traversal
	•	JSON data handling
	•	Timestamp management
	•	Command-line interaction

⸻

What the Tool Does

The File Integrity Checker works by performing the following major functions:
	1.	Baseline Creation
When initiated in “create” mode, the tool scans a directory and computes hash values for every file within it. The hash values represent the contents of each file in a way that even the smallest change would result in a completely different hash. These hashes, along with file paths and timestamps, are stored in a JSON file, which acts as the baseline or trusted snapshot of the directory.
	2.	Integrity Verification
In “verify” mode, the tool loads the previously saved baseline and re-scans the directory. It recalculates the hashes of existing files and compares them against the baseline. It identifies:
	•	Changed files: Files whose hash does not match the one in the baseline.
	•	New files: Files that were not in the baseline but are now present.
	•	Missing files: Files that were present in the baseline but are no longer found.

This allows users to know exactly what files have been altered, helping them detect intrusions, corruption, or unauthorized modifications.

⸻

Importance of Hashing in Integrity Checking

Hashing is a process of converting data into a fixed-size string of characters, which is typically a hexadecimal number. Cryptographic hash functions like SHA-256 ensure that:
	•	The same input always produces the same hash.
	•	It is computationally infeasible to reverse the hash back to the original input.
	•	Any change in the input, however minor, results in a drastically different hash.

This makes hash functions ideal for file integrity checking, as any unauthorized or accidental change in a file will be detected through hash mismatch.

⸻

Practical Use Cases
	•	System Security: Detects malicious tampering with system files or configuration files.
	•	Software Development: Monitors changes in code files to ensure unauthorized edits are caught.
	•	Digital Forensics: Provides evidence of when and how files were altered or accessed.
	•	Data Backup Verification: Ensures backup files are identical to the source files.

⸻

Project Deliverables

The final deliverable is a command-line Python script that allows users to:
	•	Create a baseline of file states in a specified directory.
	•	Verify current file states against the saved baseline.
	•	Generate readable output highlighting changes in the file structure.

This utility promotes awareness, accountability, and security in managing files and directories.
