# 🔒 FileScope

**FileScope** is a cybersecurity tool for analyzing files and detecting risks. Ideal for malware triage, suspicious file checks, and security training.

**Features:** SHA256 hash, file header & extension check, size anomaly detection, optional VirusTotal scan, basic risk assessment.

**Usage:**  
`python filescope.py file.pdf`  
`python filescope.py file.pdf --vt-api-key YOUR_API_KEY`  
`python filescope.py ./files --batch`

**Flags:** Executables disguised as documents, extension mismatches, large files, VirusTotal detections.

**Disclaimer:** Educational use only; not a replacement for antivirus.
