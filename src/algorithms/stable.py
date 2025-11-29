"""
Une extension stable est :
    - Sans conflit
    - Attaque tous les arguments hors de l'ensemble
"""
def enumerate_stable(af):
    """
    Retourne la liste des extensions stables (ensembles d'arguments).
    """
    A = list(af.A)
    stables = []

    def attacks_all_outside(S):
        outside = af.A - S
        return all(any((x, a) in af.R for x in S) for a in outside)

    def dfs(i, current):
        if i == len(A):
            if af.conflict_free(current) and attacks_all_outside(current):
                stables.append(set(current))
            return
        a = A[i]
        # Inclure a
        cand = set(current); cand.add(a)
        if af.conflict_free(cand):  # pruning
            dfs(i+1, cand)
        # Exclure a
        dfs(i+1, current)

    dfs(0, set())
    return stables
