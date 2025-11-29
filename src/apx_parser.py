import re
from src.af import AF

'''
On va lire le fichier .apx ligne par ligne
D'abord on vérifie que chaque ligne respecte le format
    - arg(x). pour un argument.
    - att(x,y). pour une attaque.
On va construire deux sets :
    - arguments : tous les noms d'arguments
    - attaques : couples (x,y) représentant 'x attaque y'
Retourner un objet AF (la structure d’argumentation).
'''

ARG_RE = re.compile(r"^arg\(([A-Za-z0-9_]+)\)\.$")
ATT_RE = re.compile(r"^att\(([A-Za-z0-9_]+),([A-Za-z0-9_]+)\)\.$")

def load_af(path):
    arguments = set()
    attacks = set()

    with open(path, "r") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            m_arg = ARG_RE.match(line)
            m_att = ATT_RE.match(line)
            if m_arg:
                arg_name = m_arg.group(1)
                # Vérifier noms interdits
                if arg_name in {"arg", "att"}:
                    raise ValueError(f"Nom d'argument interdit: '{arg_name}' (ligne {ln})")

                # Vérifier doublons
                if arg_name in arguments:
                    raise ValueError(f"Argument dupliqué: '{arg_name}' (ligne {ln})")

                arguments.add(arg_name)
            elif m_att:
                x, y = m_att.groups()
                # Vérifier noms interdits
                if x in {"arg", "att"} or y in {"arg", "att"}:
                    raise ValueError(f"Nom d'argument interdit dans attaque: '{x},{y}' (ligne {ln})")

                # Vérifier que les arguments sont déclarés avant
                if x not in arguments or y not in arguments:
                    raise ValueError(f"Attaque avec argument non déclaré: '{x},{y}' (ligne {ln})")

                if x not in arguments or y not in arguments:
                    raise ValueError(f"Attaque avec argument non déclaré: {line}")

                attacks.add((x, y))
            else:
                raise ValueError(f"Ligne invalide: {line}")

    return AF(arguments, attacks)