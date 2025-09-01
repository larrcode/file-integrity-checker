import hashlib, os, sys
from pathlib import Path

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 2:
        print("Usage: python file_integrity_checker.py <path-to-file>")
        return

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    sidecar = file_path.with_suffix(file_path.suffix + ".sha256")
    current = sha256_of(file_path)

    if not sidecar.exists():
        # First run: save baseline
        sidecar.write_text(current)
        print(f"Baseline saved to {sidecar}")
        print(f"SHA-256: {current}")
    else:
        # Verify against baseline
        baseline = sidecar.read_text().strip()
        print(f"Current : {current}")
        print(f"Baseline: {baseline}")
        if current == baseline:
            print("Integrity Check: ✅ File is unchanged")
        else:
            print("Integrity Check: ❌ File has been modified")

if __name__ == "__main__":
    main()
