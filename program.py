import argparse
from src.apx_parser import load_af
from src.semantics import handle_query

def main():
    parser = argparse.ArgumentParser(description="Solveur d'argumentation (Préférée / Stable)")
    parser.add_argument("-p", required=True, help="Type de requête (VE-PR, VE-ST, DC-PR, DS-PR, DC-ST, DS-ST)")
    parser.add_argument("-f", required=True, help="Chemin du fichier .apx")
    parser.add_argument("-a", required=True, help="Arguments de la requête (ex: a,c,d ou a)")
    args = parser.parse_args()

    # Charger le système d'argumentation
    af = load_af(args.f)

    # Exécuter la requête
    try:
        result = handle_query(af, args.p, args.a)
        print("YES" if result else "NO")
    except ValueError as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()