from pathlib import Path

from src.apx_parser import load_af

def test_parser():
    print("=== Test 1 : fichier valide ===")
    data_dir = Path(__file__).resolve().parent / "data"
    file_path = data_dir / "test_af1.apx"

    try:
        af = load_af(file_path)
        print("Test réussi !")
        print("Arguments :", af.A)
        print("Attaques  :", af.R)

        assert isinstance(af.A, set)
        assert isinstance(af.R, set)
        assert len(af.A) > 0
        print("Assertions OK\n")
    except Exception as e:
        print("Erreur :", e, "\n")

    # Test du nom d’argument interdit (arg / att)
    print("=== Test 2 : argument interdit ===")
    bad_file_1 = data_dir / "test_bad_forbidden.apx"
    with open(bad_file_1, "w") as f:
        f.write("arg(arg).\n")  # nom interdit

    try:
        load_af(bad_file_1)
        print("Échec : aucune erreur levée alors qu’un nom interdit est utilisé")
    except Exception as e:
        print("Erreur détectée comme prévu :", e, "\n")

    # Test de l'argument dupliqué
    print("=== Test 3 : argument dupliqué ===")
    bad_file_2 = data_dir / "test_bad_duplicate.apx"
    with open(bad_file_2, "w") as f:
        f.write("arg(a).\narg(a).\n")  # duplication

    try:
        load_af(bad_file_2)
        print("Échec : aucune erreur levée alors qu’un argument est dupliqué")
    except Exception as e:
        print("Erreur détectée comme prévu :", e, "\n")


if __name__ == "__main__":
    test_parser()
