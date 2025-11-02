from openfisca_core.model_api import *
from openfisca_nouvelle_caledonie.entities import Individu
from openfisca_nouvelle_caledonie.variables.revenus.activite.fonction_publique import (
    __ForwardVariable,
)


class prime_speciale_points(__ForwardVariable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime spéciale pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"


class prime_speciale(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime spéciale pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"

    def formula(individu, period, parameters):
        direction = individu("employeur_public_direction", period)
        elig = (direction == "G0901110") + (direction == "G0600000")

        nb = individu("prime_speciale_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        type_fonction_publique = individu("type_fonction_publique", period)
        valeur_point = parameters(period).remuneration_fonction_publique.valeur_point[
            type_fonction_publique
        ]
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return elig * (
            nb * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class prime_technicite_points(__ForwardVariable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime spéciale pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"


class prime_technicite(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime technique pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"

    def formula(individu, period, parameters):
        direction = individu("employeur_public_direction", period)
        elig = (direction == "G0901110") + (direction == "G0600000")

        nb = individu("prime_technicite_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        type_fonction_publique = individu("type_fonction_publique", period)
        valeur_point = parameters(period).remuneration_fonction_publique.valeur_point[
            type_fonction_publique
        ]
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return elig * (
            nb * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class prime_speciale_technicite_points(__ForwardVariable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les dir DITTT, DIMENC, DINUM, DAVAR + filière technique des domaines rural, équipement, informatiques, si pas de prime équivalente"
    reference = "Délib n°358 et n°359 du 18/01/2008, 417 du 26/11/2008"


class prime_speciale_technicite(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les dir DITTT, DIMENC, DINUM, DAVAR + filière technique des domaines rural, équipement, informatiques, si pas de prime équivalente"
    reference = "Délib n°358 et n°359 du 18/01/2008, 417 du 26/11/2008"

    def formula(individu, period, parameters):
        direction = individu("employeur_public_direction", period)
        elig_direction = (
            sum(
                [
                    direction == d
                    for d in ["G1400000", "G1300000", "G9800000", "G0800000"]
                ]
            )
            > 0
        )

        domaine = individu("echelon_domaine", period)
        prime_technicite = individu("prime_technicite", period)
        elig_domaine = (
            sum([domaine == d for d in ["ER", "EQ", "IN"]]) * (prime_technicite == 0)
            > 0
        )
        elig = elig_direction + elig_domaine

        nb = individu("prime_speciale_technicite_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        type_fonction_publique = individu("type_fonction_publique", period)
        valeur_point = parameters(period).remuneration_fonction_publique.valeur_point[
            type_fonction_publique
        ]
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return elig * (
            nb * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class prime_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Prime pour catégorie A dans le secteur public"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        cat = individu("categorie_fonction_publique", period)
        prime = parameters(period).remuneration_fonction_publique.prime[cat]

        temps_de_travail = individu("temps_de_travail", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        type_fonction_publique = individu("type_fonction_publique", period)
        valeur_point = parameters(period).remuneration_fonction_publique.valeur_point[
            type_fonction_publique
        ]

        est_retraite = individu("est_retraite", period)

        return not_(est_retraite) * (
            prime * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class primes_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Primes dans le secteur public"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period):
        noms = [
            "prime_fonction_publique",
            "prime_speciale",
            "prime_technicite",
            "prime_speciale_technicite",
        ]

        return sum([individu(prime, period) for prime in noms])
