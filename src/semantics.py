from src.algorithms.preferred import enumerate_preferred
from src.algorithms.stable import enumerate_stable
from src.utils import normalize_name

def is_preferred_extension(af, S: set[str]) -> bool:
    """
    Vérifie si S est une extension préférée.
    """
    prefs = enumerate_preferred(af)
    return S in prefs

def is_stable_extension(af, S: set[str]) -> bool:
    """
    Vérifie si S est une extension stable.
    """
    stabs = enumerate_stable(af)
    return S in stabs

def credulous_acceptance(af, a: str, semantics: str) -> bool:
    """
    Vérifie si l'argument a est accepté de manière crédible (au moins une extension).
    semantics = 'PR' ou 'ST'
    """
    exts = enumerate_preferred(af) if semantics == "PR" else enumerate_stable(af)
    return any(a in S for S in exts)

def skeptical_acceptance(af, a: str, semantics: str) -> bool:
    """
    Vérifie si l'argument a est accepté de manière sceptique (toutes les extensions).
    semantics = 'PR' ou 'ST'
    """
    exts = enumerate_preferred(af) if semantics == "PR" else enumerate_stable(af)
    return len(exts) > 0 and all(a in S for S in exts)

def handle_query(af, task: str, arg_input: str) -> bool:
    """
    Route la requête en fonction du code -p (VE-PR, DC-ST, etc.)
    """
    task = task.upper()
    if task == "VE-PR":
        S = {normalize_name(a) for a in arg_input.split(",")}
        unknown = S - af.A
        if unknown:
            raise ValueError(f"Arguments inconnus: {','.join(sorted(unknown))}")
        return is_preferred_extension(af, S)
    elif task == "VE-ST":
        S = {normalize_name(a) for a in arg_input.split(",")}
        unknown = S - af.A
        if unknown:
            raise ValueError(f"Arguments inconnus: {','.join(sorted(unknown))}")
        return is_stable_extension(af, S)
    elif task == "DC-PR":
        arg = normalize_name(arg_input)
        if arg not in af.A:
            raise ValueError(f"Argument inconnu: {arg_input}")
        return credulous_acceptance(af, arg, "PR")
    elif task == "DS-PR":
        arg = normalize_name(arg_input)
        if arg not in af.A:
            raise ValueError(f"Argument inconnu: {arg_input}")
        return skeptical_acceptance(af, arg, "PR")
    elif task == "DC-ST":
        arg = normalize_name(arg_input)
        if arg not in af.A:
            raise ValueError(f"Argument inconnu: {arg_input}")
        return credulous_acceptance(af, arg, "ST")
    elif task == "DS-ST":
        arg = normalize_name(arg_input)
        if arg not in af.A:
            raise ValueError(f"Argument inconnu: {arg_input}")
        return skeptical_acceptance(af, arg, "ST")
    else:
        raise ValueError(f"Tâche inconnue: {task}")
