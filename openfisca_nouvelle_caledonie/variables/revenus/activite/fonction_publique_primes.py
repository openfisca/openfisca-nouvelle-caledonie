"""Primes dans la fonction publique."""

import numpy as np
from numpy.core.defchararray import startswith

from openfisca_core.model_api import *
from openfisca_nouvelle_caledonie.entities import Individu
from openfisca_nouvelle_caledonie.variables.revenus.activite.fonction_publique import (
    CategorieFonctionPublique,
)


class prime_speciale_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime spéciale pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_speciale.points


class prime_speciale(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime spéciale pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"

    def formula(individu, period):
        direction = individu("employeur_public_direction", period)
        elig = (direction == "G0901110") + (direction == "G0600000")

        nb = individu("prime_speciale_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return elig * (
            nb * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class prime_technicite_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime spéciale pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_technicite.points


class prime_technicite(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime technique pour la DRHFPNC et la DBAF"
    reference = "Délib 405 du 21/08/2008 et 440 du 30/12/2008"

    def formula(individu, period):
        direction = individu("employeur_public_direction", period)
        elig = (direction == "G0901110") + (direction == "G0600000")

        nb = individu("prime_technicite_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return elig * (
            nb * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class prime_speciale_technicite_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les dir DITTT, DIMENC, DINUM, DAVAR + filière technique des domaines rural, équipement, informatiques, si pas de prime équivalente"
    reference = "Délib n°358 et n°359 du 18/01/2008, 417 du 26/11/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_speciale_technicite.points


class prime_speciale_technicite(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les dir DITTT, DIMENC, DINUM, DAVAR + filière technique des domaines rural, équipement, informatiques, si pas de prime équivalente"
    reference = "Délib n°358 et n°359 du 18/01/2008, 417 du 26/11/2008"

    def formula(individu, period):
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
        valeur_point = individu("valeur_point", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return elig * (
            nb * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class prime_territoriale_a_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les ingénieurs de la filière technique (hors aviation civil et météo dans leurs directions)"
    reference = "Délib 74/CP du 12/02/2009"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_territoriale_a.points


class prime_territoriale_a(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les ingénieurs de la filière technique (hors aviation civil et météo dans leurs directions)"
    reference = "Délib 74/CP du 12/02/2009"

    def formula(individu, period):
        echelon = individu("echelon", period)
        grille_ok = startswith(list(echelon), "FTIN")  # TO-DO

        direction = individu("employeur_public_direction", period)
        direction_ok = (direction != "GM030000") * (direction != "MF-000")
        elig = grille_ok * direction_ok

        nb = individu("prime_territoriale_a_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return (
            elig
            * nb
            * valeur_point
            * temps_de_travail
            * taux_indexation_fonction_publique
        )


class prime_territoriale_b_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les techniciens de la filière technique (hors aviation civil et météo dans leurs directions)"
    reference = "Délib 74/CP du 12/02/2009"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_territoriale_b.points


class prime_territoriale_b(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les techniciens de la filière technique (hors aviation civil et météo dans leurs directions)"
    reference = "Délib 74/CP du 12/02/2009"

    def formula(individu, period):
        echelon = individu("echelon", period)
        grille_ok = startswith(list(echelon), "FTTE")  # TO-DO

        direction = individu("employeur_public_direction", period)
        direction_ok = (direction != "GM030000") * (direction != "MF-000")
        elig = grille_ok * direction_ok

        nb = individu("prime_territoriale_b_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return (
            elig
            * nb
            * valeur_point
            * temps_de_travail
            * taux_indexation_fonction_publique
        )


class prime_territoriale_c_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les techniciens de la filière technique (hors aviation civil et météo dans leurs directions)"
    reference = "Délib 74/CP du 12/02/2009"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_territoriale_c.points


class prime_territoriale_c(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime pour les techniciens de la filière technique (hors aviation civil et météo dans leurs directions)"
    reference = "Délib 74/CP du 12/02/2009"

    def formula(individu, period):
        echelon = individu("echelon", period)
        grille_ok = startswith(list(echelon), "FTTA")  # TO-DO

        direction = individu("employeur_public_direction", period)
        direction_ok = (direction != "GM030000") * (direction != "MF-000")
        elig = grille_ok * direction_ok

        nb = individu("prime_territoriale_c_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        return (
            elig
            * nb
            * valeur_point
            * temps_de_travail
            * taux_indexation_fonction_publique
        )


class prime_direction_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime des personnels de direction"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_direction.points


class prime_direction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime des personnels de direction"

    def formula(individu, period):
        fonction = individu("employeur_public_fonction", period)
        elig = sum([fonction == f for f in ["T4DR", "T4DI", "T4A1"]])

        nb = individu("prime_direction_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation = individu("taux_indexation_fonction_publique", period)
        return elig * (nb * valeur_point * temps_de_travail * taux_indexation)


class prime_adjoint_direction_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime des personnels adjoints de direction"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_adjoint_direction.points


class prime_adjoint_direction(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime des personnels adjoints de direction"

    def formula(individu, period):
        fonction = individu("employeur_public_fonction", period)
        elig = sum([fonction == f for f in ["T4DA", "T4DT", "T4A2"]])

        nb = individu("prime_adjoint_direction_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation = individu("taux_indexation_fonction_publique", period)
        return elig * (nb * valeur_point * temps_de_travail * taux_indexation)


class prime_sujetion_cadre_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime des personnels d’encadrement et assimilés"
    reference = "Délib 393 du 25/06/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_sujetion_cadre.points


class prime_sujetion_cadre(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime des personnels d’encadrement et assimilés"
    reference = "Délib 393 du 25/06/2008"

    def formula(individu, period):
        fonction = individu("employeur_public_fonction", period)
        elig = sum([fonction == f for f in ["T4A3", "T4SC", "T4SI"]])

        nb = individu("prime_sujetion_cadre_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation = individu("taux_indexation_fonction_publique", period)
        return elig * (nb * valeur_point * temps_de_travail * taux_indexation)


class prime_sujetion_chef_secteur_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Indemnités de sujétion des personnels de direction des services publics de la Nouvelle-Calédonie"
    reference = "Délib 218 du 8/11/2006"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_sujetion_chef_secteur.points


class prime_sujetion_chef_secteur(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Indemnités de sujétion des personnels de direction des services publics de la Nouvelle-Calédonie"
    reference = "Délib 218 du 8/11/2006"

    def formula(individu, period):
        fonction = individu("employeur_public_fonction", period)
        elig = sum([fonction == f for f in ["T4CS", "T4A8", "T4A5"]])

        nb = individu("prime_sujetion_chef_secteur_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation = individu("taux_indexation_fonction_publique", period)
        return elig * (nb * valeur_point * temps_de_travail * taux_indexation)


class prime_sujetion_chef_bureau_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Indemnités de sujétion des personnels de direction des services publics de la Nouvelle-Calédonie"
    reference = "Délib 218 du 8/11/2006"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_sujetion_chef_bureau.points


class prime_sujetion_chef_bureau(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Indemnités de sujétion des personnels de direction des services publics de la Nouvelle-Calédonie"
    reference = "Délib 218 du 8/11/2006"

    def formula(individu, period):
        fonction = individu("employeur_public_fonction", period)
        elig = sum([fonction == f for f in ["T4CB", "T4CI"]])

        nb = individu("prime_sujetion_chef_bureau_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation = individu("taux_indexation_fonction_publique", period)
        return elig * (nb * valeur_point * temps_de_travail * taux_indexation)


class prime_sujetion_charge_mission_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Indemnité pour chargé de mission"
    reference = "Délib 393 du 25/06/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_sujetion_charge_mission.points


class prime_sujetion_charge_mission(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Indemnité pour chargé de mission"
    reference = "Délib 393 du 25/06/2008"

    def formula(individu, period):
        fonction = individu("employeur_public_fonction", period)
        elig = sum([fonction == f for f in ["T4CM"]])

        nb = individu("prime_sujetion_charge_mission_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        taux_indexation = individu("taux_indexation_fonction_publique", period)
        return elig * (nb * valeur_point * temps_de_travail * taux_indexation)


class prime_aviation_technicite(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime de l'aviation civile et météorologie"
    reference = "Délib 170 du 29/03/2006"

    def formula(individu, period, parameters):
        echelle = individu("employeur_public_echelle", period)
        tch = parameters(period).marche_travail.remuneration_fonction_publique.tch
        temps_de_travail = individu("temps_de_travail", period)

        indexes = np.array([e if e in tch else "ZERO" for e in echelle])

        return tch[indexes] * temps_de_travail


class prime_stabilite_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Majoration pour grille de sages-femmes"
    reference = "Délib 423 du 20/03/2019"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_stabilite.points


class prime_stabilite(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Majoration pour grille de sages-femmes"
    reference = "Délib 423 du 20/03/2019"

    def formula(individu, period):
        echelle = individu("employeur_public_echelle", period)
        elig = startswith(list(echelle), "S012")  # TO-DO

        nb = individu("prime_stabilite_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        indexation = individu("taux_indexation_fonction_publique", period)

        return elig * (nb * valeur_point * temps_de_travail * indexation)


class prime_stabilite_2_points_categorie_a(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_stabilite_2.categorie_a.points


class prime_stabilite_2_points_categorie_b(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.prime_stabilite_2.categorie_b.points


class prime_stabilite_2_points(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        echelle = individu("employeur_public_echelle", period)
        l_echelle = list(echelle)  # TO-DO
        cat_a_prefixes = [
            "S012",
            "S036",
            "S037",
            "S038",
            "PM002",
            "PM003",
            "PM004",
            "PM006",
            "PM007",
            "PM008",
            "PM029",
            "PMA10",
            "PMA12",
            "PMA13",
            "PMA17",
        ]
        cat_a = sum([startswith(l_echelle, prefix) for prefix in cat_a_prefixes])

        cat_b_prefixes = ["PM016"]
        cat_b = sum([startswith(l_echelle, prefix) for prefix in cat_b_prefixes])

        p_a = individu("prime_stabilite_2_points_categorie_a", period)
        p_b = individu("prime_stabilite_2_points_categorie_b", period)

        return cat_a * p_a + cat_b * p_b


class prime_stabilite_2(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Majoration pour grille de sages-femmes"
    reference = "Délib 423 du 20/03/2019"

    def formula(individu, period):
        employeur = individu("employeur_public", period)
        elig_employeurs = ["C1", "C2", "N2", "S1", "N1", "I1", "T4"]
        elig = sum([elig_employeur == employeur for elig_employeur in elig_employeurs])

        nb = individu("prime_stabilite_2_points", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)
        indexation = individu("taux_indexation_fonction_publique", period)

        return elig * nb * valeur_point * temps_de_travail * indexation


class prime_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Prime pour catégorie A dans le secteur public"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        cat = individu("categorie_fonction_publique", period)
        prime = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.categorie[cat]

        temps_de_travail = individu("temps_de_travail", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        valeur_point = individu("valeur_point", period)

        est_retraite = individu("est_retraite", period)

        return not_(est_retraite) * (
            prime * valeur_point * temps_de_travail * taux_indexation_fonction_publique
        )


class prime_experimentale_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité à la prime expérimentale dans la fonction publique"

    def formula(individu, period, parameters):
        P = parameters(period).remuneration_fonction_publique.prime.prime_experimentale
        cat = individu("categorie_fonction_publique", period)
        C = CategorieFonctionPublique
        categories = P.categories
        elig_cat = (
            (cat == C.categorie_a) * categories.a
            + (cat == C.categorie_b) * categories.b
            + (cat == C.categorie_c) * categories.c
            + (cat == C.categorie_d) * categories.d
        )

        fonction = individu("employeur_public_fonction", period)
        elig_fonction = len(P.fonctions) == 0 + sum(
            [fonction == test for test in P.fonctions]
        )

        cadre = individu("cadre", period)
        elig_cadre = len(P.cadres) == 0 + sum([cadre == test for test in P.cadres])

        corps = individu("corps", period)
        elig_corps = len(P.corps) == 0 + sum([corps == test for test in P.corps])
        return elig_cat * elig_fonction * elig_cadre * elig_corps


class prime_experimentale(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Prime expérimentale dans la fonction publique"

    def formula(individu, period, parameters):
        elig = individu("prime_experimentale_eligibilite", period)
        P = parameters(period).remuneration_fonction_publique.prime.prime_experimentale

        valeur_point = individu("valeur_point", period)
        coefficient_point = P.coefficient_point
        montant = P.montant

        bool_temp_partiel = P.prise_en_compte_temps_partiel
        temps_de_travail = individu("temps_de_travail", period)
        coef_temps = (1 - bool_temp_partiel) + bool_temp_partiel * temps_de_travail

        bool_indexation = P.prise_en_compte_indexation
        indexation = individu("taux_indexation_fonction_publique", period)
        coef_indexation = (1 - bool_indexation) + bool_indexation * indexation

        return (
            elig
            * (montant + coefficient_point * valeur_point)
            * coef_temps
            * coef_indexation
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
            "prime_territoriale_a",
            "prime_territoriale_b",
            "prime_territoriale_c",
            "prime_dsf_fixe",
            "prime_dsf_variable",
            "prime_direction",
            "prime_adjoint_direction",
            "prime_sujetion_cadre",
            "prime_sujetion_chef_secteur",
            "prime_sujetion_chef_bureau",
            "prime_sujetion_charge_mission",
            "prime_aviation_technicite",
            "prime_stabilite",
            "prime_stabilite_2",
            "prime_experimentale",
        ]

        return sum([individu(prime, period) for prime in noms])
