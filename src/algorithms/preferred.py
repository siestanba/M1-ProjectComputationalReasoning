"""
Une extension préféré est :
    - Admissible (sans conflit + défend ses arguments)
    - Maximale par inclusion parmi les ensembles admissibles
"""
def enumerate_preferred(af):
    """
    Retourne la liste des extensions préférées (ensembles d'arguments).
    """
    A = list(af.A)
    admissibles = []

    def dfs(i, current):
        if i == len(A):
            if af.admissible(current):
                admissibles.append(set(current))
            return
        a = A[i]
        # Inclure a
        cand = set(current); cand.add(a)
        if af.conflict_free(cand):  # pruning
            dfs(i+1, cand)
        # Exclure a
        dfs(i+1, current)

    dfs(0, set())

    # Garder seulement les maximaux
    preferred = [S for S in admissibles if not any(S < T for T in admissibles)]
    return preferred
