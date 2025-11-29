from src.algorithms.preferred import enumerate_preferred
from src.algorithms.stable import enumerate_stable

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
        S = set(arg_input.split(","))
        return is_preferred_extension(af, S)
    elif task == "VE-ST":
        S = set(arg_input.split(","))
        return is_stable_extension(af, S)
    elif task == "DC-PR":
        return credulous_acceptance(af, arg_input, "PR")
    elif task == "DS-PR":
        return skeptical_acceptance(af, arg_input, "PR")
    elif task == "DC-ST":
        return credulous_acceptance(af, arg_input, "ST")
    elif task == "DS-ST":
        return skeptical_acceptance(af, arg_input, "ST")
    else:
        raise ValueError(f"Tâche inconnue: {task}")
