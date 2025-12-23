from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "program.py"
DATA = Path(__file__).resolve().parent / "data"

def check(cmd, expected=None, description=""):
    if description:
        print(f"\n{description}")
    print(">", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout.strip()
    print("stdout:", out)
    if expected is not None:
        assert out == expected, f"Attendu {expected}, obtenu {out}"
        print("OK")
    else:
        assert out in {"YES", "NO"}, f"Sortie invalide: {out}"
        print("Sortie valide")

def main():
    print("="*60)
    print("TESTS SUR LES NOUVEAUX FICHIERS .apx")
    print("="*60)
    
    # Test AF6: self-attack + cycle b<->c
    # Extensions préférées: {b} et {c}
    # Extensions stables: aucune
    print("\n--- TEST AF6: self-attack + cycle ---")
    file6 = str(DATA / "test_af6.apx")
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file6, "-a", "b"], 
          expected="YES", description="VE-PR: {b} est une extension préférée")
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file6, "-a", "c"], 
          expected="YES", description="VE-PR: {c} est une extension préférée")
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file6, "-a", "a"], 
          expected="NO", description="VE-PR: {a} n'est pas une extension préférée (self-attack)")
    check([sys.executable, str(PROGRAM), "-p", "DC-PR", "-f", file6, "-a", "b"], 
          expected="YES", description="DC-PR: b est accepté de manière crédible")
    check([sys.executable, str(PROGRAM), "-p", "DS-PR", "-f", file6, "-a", "a"], 
          expected="NO", description="DS-PR: a n'est dans aucune extension")
    check([sys.executable, str(PROGRAM), "-p", "VE-ST", "-f", file6, "-a", "b"], 
          expected="NO", description="VE-ST: pas d'extension stable")
    check([sys.executable, str(PROGRAM), "-p", "DC-ST", "-f", file6, "-a", "b"], 
          expected="NO", description="DC-ST: pas d'extension stable")
    
    # Test AF7: chaîne x->y->z
    # Extensions préférées et stables: {x,z}
    print("\n--- TEST AF7: chaîne linéaire ---")
    file7 = str(DATA / "test_af7.apx")
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file7, "-a", "x,z"], 
          expected="YES", description="VE-PR: {x,z} est une extension préférée")
    check([sys.executable, str(PROGRAM), "-p", "VE-ST", "-f", file7, "-a", "x,z"], 
          expected="YES", description="VE-ST: {x,z} est une extension stable")
    check([sys.executable, str(PROGRAM), "-p", "DC-PR", "-f", file7, "-a", "y"], 
          expected="NO", description="DC-PR: y n'est pas accepté")
    check([sys.executable, str(PROGRAM), "-p", "DS-PR", "-f", file7, "-a", "x"], 
          expected="YES", description="DS-PR: x est dans toutes les extensions")
    check([sys.executable, str(PROGRAM), "-p", "DS-ST", "-f", file7, "-a", "z"], 
          expected="YES", description="DS-ST: z est dans toutes les extensions stables")
    
    # Test AF8: argument unique sans attaque
    # Extensions préférées et stables: {p}
    print("\n--- TEST AF8: argument isolé ---")
    file8 = str(DATA / "test_af8.apx")
    check([sys.executable, str(PROGRAM), "-p", "VE-PR", "-f", file8, "-a", "p"], 
          expected="YES", description="VE-PR: {p} est une extension préférée")
    check([sys.executable, str(PROGRAM), "-p", "VE-ST", "-f", file8, "-a", "p"], 
          expected="YES", description="VE-ST: {p} est une extension stable")
    check([sys.executable, str(PROGRAM), "-p", "DS-PR", "-f", file8, "-a", "p"], 
          expected="YES", description="DS-PR: p est dans toutes les extensions")
    check([sys.executable, str(PROGRAM), "-p", "DS-ST", "-f", file8, "-a", "p"], 
          expected="YES", description="DS-ST: p est dans toutes les extensions stables")
    
    # Test AF9: cycle impair m->n->o->m
    # Extensions préférées: {} (vide)
    # Extensions stables: aucune
    print("\n--- TEST AF9: cycle impair ---")
    file9 = str(DATA / "test_af9.apx")
    check([sys.executable, str(PROGRAM), "-p", "DC-PR", "-f", file9, "-a", "m"], 
          expected="NO", description="DC-PR: m n'est pas accepté")
    check([sys.executable, str(PROGRAM), "-p", "DC-ST", "-f", file9, "-a", "n"], 
          expected="NO", description="DC-ST: n n'est pas accepté (pas d'extension stable)")
    check([sys.executable, str(PROGRAM), "-p", "DS-PR", "-f", file9, "-a", "o"], 
          expected="NO", description="DS-PR: o n'est dans aucune extension")
    
    print("\n" + "="*60)
    print("TOUS LES TESTS SONT PASSÉS ✓")
    print("="*60)

if __name__ == "__main__":
    main()
