#!/usr/bin/env python3
"""
FileScope - Defensive File Analysis Tool
A legitimate cybersecurity tool for analyzing files to detect potential threats
"""

import os
import hashlib
import magic
import requests
import json
import time
from pathlib import Path
import argparse
import sys

class FileAnalyzer:
    def __init__(self):
        self.known_malicious_headers = {
            b'MZ': 'Windows Executable (PE)',
            b'\x7fELF': 'Linux Executable (ELF)',
            b'\xca\xfe\xba\xbe': 'Java Class File',
            b'PK\x03\x04': 'ZIP Archive',
            b'Rar!': 'RAR Archive'
        }
        
        self.safe_headers = {
            b'%PDF': 'PDF Document',
            b'\x89PNG': 'PNG Image',
            b'\xff\xd8\xff': 'JPEG Image',
            b'GIF8': 'GIF Image',
            b'PK\x03\x04': 'Office Document (if in .docx/.xlsx)',
            b'\xd0\xcf\x11\xe0': 'Microsoft Office Document'
        }

    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"Error calculating hash: {e}"

    def analyze_file_header(self, filepath):
        """Analyze file header to determine actual file type"""
        try:
            with open(filepath, 'rb') as f:
                header = f.read(16)
            
            results = []
            for signature, description in self.known_malicious_headers.items():
                if header.startswith(signature):
                    results.append(f"⚠️  DETECTED: {description}")
            
            for signature, description in self.safe_headers.items():
                if header.startswith(signature):
                    results.append(f"✅ SAFE: {description}")
            
            if not results:
                results.append("❓ Unknown file type - exercise caution")
            
            return results
            
        except Exception as e:
            return [f"Error reading file header: {e}"]

    def check_file_size_anomaly(self, filepath):
        """Check for unusually large file sizes that might indicate padding"""
        try:
            file_size = os.path.getsize(filepath)
            file_ext = Path(filepath).suffix.lower()
            
            # Define normal size ranges for common file types (in MB)
            normal_sizes = {
                '.pdf': 50,
                '.doc': 20,
                '.docx': 20,
                '.xls': 30,
                '.xlsx': 30,
                '.txt': 5,
                '.jpg': 10,
                '.png': 10,
                '.gif': 5
            }
            
            size_mb = file_size / (1024 * 1024)
            
            if file_ext in normal_sizes:
                if size_mb > normal_sizes[file_ext]:
                    return f"⚠️  SUSPICIOUS: File size ({size_mb:.1f}MB) unusually large for {file_ext} file"
                else:
                    return f"✅ File size ({size_mb:.1f}MB) appears normal for {file_ext}"
            else:
                return f"ℹ️  File size: {size_mb:.1f}MB (unknown extension)"
                
        except Exception as e:
            return f"Error checking file size: {e}"

    def check_extension_mismatch(self, filepath):
        """Check if file extension matches actual file type"""
        try:
            # Get file extension
            file_ext = Path(filepath).suffix.lower()
            
            # Use python-magic to detect actual file type
            actual_type = magic.from_file(filepath, mime=True)
            
            # Common extension to MIME type mappings
            expected_types = {
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.txt': 'text/plain',
                '.exe': 'application/x-executable',
                '.zip': 'application/zip'
            }
            
            if file_ext in expected_types:
                expected = expected_types[file_ext]
                if actual_type == expected:
                    return f"✅ Extension matches file type: {actual_type}"
                else:
                    return f"⚠️  MISMATCH: Extension says {file_ext} but file is {actual_type}"
            else:
                return f"ℹ️  Detected file type: {actual_type}"
                
        except Exception as e:
            return f"Error detecting file type: {e}"

    def check_virustotal(self, file_hash, api_key=None):
        """Check file hash against VirusTotal (requires API key)"""
        if not api_key:
            return "ℹ️  VirusTotal check skipped (no API key provided)"
        
        try:
            url = f"https://www.virustotal.com/vtapi/v2/file/report"
            params = {'apikey': api_key, 'resource': file_hash}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result['response_code'] == 1:
                    positives = result['positives']
                    total = result['total']
                    if positives > 0:
                        return f"⚠️  VirusTotal: {positives}/{total} engines detected threats"
                    else:
                        return f"✅ VirusTotal: Clean ({total} engines)"
                else:
                    return "ℹ️  File not found in VirusTotal database"
            else:
                return f"❌ VirusTotal API error: {response.status_code}"
                
        except Exception as e:
            return f"Error contacting VirusTotal: {e}"

    def analyze_file(self, filepath, vt_api_key=None):
        """Main analysis function"""
        if not os.path.exists(filepath):
            return f"Error: File '{filepath}' not found"
        
        print(f"\n🔍 Analyzing: {filepath}")
        print("=" * 60)
        
        # Basic file info
        file_size = os.path.getsize(filepath)
        print(f"📁 File size: {file_size:,} bytes ({file_size/(1024*1024):.2f} MB)")
        
        # Calculate hash
        file_hash = self.calculate_file_hash(filepath)
        print(f"🔐 SHA256: {file_hash}")
        
        # Header analysis
        print(f"\n📋 Header Analysis:")
        header_results = self.analyze_file_header(filepath)
        for result in header_results:
            print(f"   {result}")
        
        # Extension check
        print(f"\n🏷️  Extension Analysis:")
        ext_result = self.check_extension_mismatch(filepath)
        print(f"   {ext_result}")
        
        # Size anomaly check
        print(f"\n📏 Size Analysis:")
        size_result = self.check_file_size_anomaly(filepath)
        print(f"   {size_result}")
        
        # VirusTotal check
        print(f"\n🛡️  VirusTotal Check:")
        vt_result = self.check_virustotal(file_hash, vt_api_key)
        print(f"   {vt_result}")
        
        # Risk assessment
        print(f"\n🎯 Risk Assessment:")
        self.assess_risk(header_results, ext_result, size_result, vt_result)

    def assess_risk(self, header_results, ext_result, size_result, vt_result):
        """Provide overall risk assessment"""
        risk_factors = []
        
        # Check for executables disguised as documents
        for result in header_results:
            if "DETECTED:" in result and ("Executable" in result or "PE" in result):
                risk_factors.append("File appears to be executable")
        
        # Check for mismatches
        if "MISMATCH:" in ext_result:
            risk_factors.append("Extension doesn't match file type")
        
        # Check for size anomalies
        if "SUSPICIOUS:" in size_result:
            risk_factors.append("Unusual file size detected")
        
        # Check VirusTotal results
        if "detected threats" in vt_result:
            risk_factors.append("Detected by antivirus engines")
        
        if risk_factors:
            print("   🚨 HIGH RISK - Multiple warning signs detected:")
            for factor in risk_factors:
                print(f"      • {factor}")
            print("   ⚠️  RECOMMENDATION: DO NOT OPEN this file")
        else:
            print("   ✅ LOW RISK - No obvious warning signs detected")
            print("   ℹ️  Still exercise caution with files from unknown sources")

def main():
    parser = argparse.ArgumentParser(description="FileScope - Defensive File Analysis Tool")
    parser.add_argument("file", help="Path to file to analyze")
    parser.add_argument("--vt-api-key", help="VirusTotal API key for enhanced scanning")
    parser.add_argument("--batch", action="store_true", help="Batch mode for multiple files")
    
    args = parser.parse_args()
    
    analyzer = FileAnalyzer()
    
    if args.batch:
        # Batch mode - analyze all files in directory
        if os.path.isdir(args.file):
            for file_path in Path(args.file).iterdir():
                if file_path.is_file():
                    analyzer.analyze_file(str(file_path), args.vt_api_key)
                    print("\n" + "="*60)
        else:
            print("Batch mode requires a directory path")
    else:
        # Single file mode
        analyzer.analyze_file(args.file, args.vt_api_key)

if __name__ == "__main__":
    print("🔒 FileScope - Defensive File Analysis Tool")
    print("📋 For cybersecurity education and file safety verification")
    print("⚠️  Always exercise caution with files from unknown sources\n")
    
    # Check if required dependencies are available
    try:
        import magic
    except ImportError:
        print("❌ Missing dependency: python-magic")
        print("   Install with: pip install python-magic")
        print("   On Windows, also: pip install python-magic-bin")
        sys.exit(1)
    
    try:
        import requests
    except ImportError:
        print("❌ Missing dependency: requests")
        print("   Install with: pip install requests")
        sys.exit(1)
    
    main()
