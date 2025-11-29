from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "program.py"
DATA = Path(__file__).resolve().parent / "data"

def check(cmd, expected=None):
    print(">", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout.strip()
    print("stdout:", out)
    if expected is not None:
        assert out == expected, f"Attendu {expected}, obtenu {out}"
    else:
        assert out in {"YES", "NO"}, f"Sortie invalide: {out}"

def main():
    file1 = str(DATA / "test_af1.apx")
    # Exemples du sujet (adapter au besoin):
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file1, "-a", "a,c,d"], expected="YES")
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file1, "-a", "a"], expected="NO")
    check([sys.executable, str(PROGRAM), "-p", "DS-PR", "-f", file1, "-a", "a"], expected="YES")
    check([sys.executable, str(PROGRAM), "-p", "DC-PR", "-f", file1, "-a", "b"], expected="NO")

    # Exemple stable (si tu connais l’attendu pour test_af2.apx, mets expected)
    file2 = str(DATA / "test_af2.apx")
    check([sys.executable, str(PROGRAM), "-p", "VE-ST", "-f", file2, "-a", "a,b"])  # sans expected
    check([sys.executable, str(PROGRAM), "-p", "DC-ST", "-f", file2, "-a", "a"])   # sans expected
    check([sys.executable, str(PROGRAM), "-p", "DS-ST", "-f", file2, "-a", "b"])   # sans expected

if __name__ == "__main__":
    main()
