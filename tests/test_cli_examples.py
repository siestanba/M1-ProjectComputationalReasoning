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
    # Attendus alignés sur tests/data/test_af1.apx : extensions préf./stables = {a,d} ou {b,d}
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file1, "-a", "a,d"], expected="YES")
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file1, "-a", "a"], expected="NO")
    check([sys.executable, str(PROGRAM), "-p", "DS-PR", "-f", file1, "-a", "a"], expected="NO")
    check([sys.executable, str(PROGRAM), "-p", "DC-PR", "-f", file1, "-a", "b"], expected="YES")

    # Stable sur test_af2.apx : extensions = {a,e},{a,d},{b,e},{b,d}
    file2 = str(DATA / "test_af2.apx")
    check([sys.executable, str(PROGRAM), "-p", "VE-ST", "-f", file2, "-a", "a,e"], expected="YES")
    check([sys.executable, str(PROGRAM), "-p", "DC-ST", "-f", file2, "-a", "c"], expected="NO")
    check([sys.executable, str(PROGRAM), "-p", "DS-ST", "-f", file2, "-a", "a"], expected="NO")

if __name__ == "__main__":
    main()
