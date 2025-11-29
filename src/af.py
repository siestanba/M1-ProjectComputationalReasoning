class AF:
    def __init__(self, arguments: set[str], attacks: set[tuple[str, str]]):
        """
        Représente un système d'argumentation abstrait.
        :param arguments: ensemble des arguments (ex: {'a','b','c'})
        :param attacks: ensemble des attaques (ex: {('a','b'),('b','c')})
        """
        self.A = arguments
        self.R = attacks

    def conflict_free(self, S: set[str]) -> bool:
        """
        Vérifie si S est sans conflit : aucun (a,b) dans R avec a,b ∈ S.
        """
        return all((a, b) not in self.R for a in S for b in S)

    def defended_by(self, S: set[str], a: str) -> bool:
        """
        Vérifie si S défend l'argument a :
        Pour chaque x qui attaque a, il existe y ∈ S qui attaque x.
        """
        attackers = [x for (x, y) in self.R if y == a]
        return all(any((d, x) in self.R for d in S) for x in attackers)

    def admissible(self, S: set[str]) -> bool:
        """
        Vérifie si S est admissible :
        - S est sans conflit
        - Chaque argument de S est défendu par S
        """
        return self.conflict_free(S) and all(self.defended_by(S, a) for a in S)
