"""Rémunération dans la fonction publique."""

from openfisca_core.indexed_enums import Enum
from openfisca_core.model_api import *
from openfisca_nouvelle_caledonie.entities import Individu


class __ForwardVariable(Variable):
    def get_formula(self, _):
        def f(entity, period):
            return entity(self.__class__.__name__, period.last_month)

        return f


class nb_mois_echelon(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        nb_mois = individu("nb_mois_echelon", period.last_month)
        echelon = individu("echelon", period)
        echelon_precedent = individu("echelon", period.last_month)
        return where(echelon == echelon_precedent, nb_mois, 0) + 1


class echelon(Variable):
    value_type = str
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        nb_mois_echelon = individu("nb_mois_echelon", period.last_month)
        p = period.last_month
        echelon = individu("echelon", p)
        P = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.echelons.meta[echelon]
        ajustement = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.ajustement_duree_echelon
        duree = P.duree_moyenne + ajustement
        suivant = P.suivant

        return where(nb_mois_echelon >= duree, suivant, echelon)


class cadre(Variable):
    value_type = str
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        echelon = individu("echelon", period)
        return [e[:2] for e in echelon]


class corps(Variable):
    value_type = str
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        echelon = individu("echelon", period)
        return [e[:5] for e in echelon]


class indice_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Indice de rémunération pour le secteur public"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        echelon = individu("echelon", period)
        echelons = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.echelons.indice
        return echelons[echelon]


class nb_mois_echelon_paie(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        nb_mois = individu("nb_mois_echelon_paie", period.last_month)
        echelon = individu("echelon_paie", period)
        echelon_precedent = individu("echelon_paie", period.last_month)
        return where(echelon == echelon_precedent, nb_mois, 0) + 1


class echelon_paie(Variable):
    value_type = str
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        nb_mois_echelon = individu("nb_mois_echelon_paie", period.last_month)
        p = period.last_month
        echelon = individu("echelon_paie", p)
        P = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.echelons.meta[echelon]
        ajustement = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.ajustement_duree_echelon
        duree = P.duree_moyenne + ajustement
        suivant = P.suivant

        return where(nb_mois_echelon >= duree, suivant, echelon)


class indice_fonction_publique_paie(Variable):
    value_type = float
    entity = Individu
    label = "Indice de rémunération pour le secteur public"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        echelon = individu("echelon_paie", period)
        echelons = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.echelons.indice
        return echelons[echelon]


class echelon_domaine(Variable):
    value_type = str
    entity = Individu
    label = "Domaine"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        echelon = individu("echelon", period)
        P = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.echelons.meta[echelon]
        return P.domaine


class CategorieFonctionPublique(Enum):
    __order__ = "categorie_a categorie_b categorie_c categorie_d non_concerne"
    categorie_a = "Categorie A"
    categorie_b = "Categorie B"
    categorie_c = "Categorie C"
    categorie_d = "Categorie D"
    non_concerne = "Non concerné"


class matricule(__ForwardVariable):
    value_type = str
    entity = Individu
    definition_period = MONTH


class categorie_fonction_publique(__ForwardVariable):
    value_type = Enum
    possible_values = CategorieFonctionPublique
    default_value = CategorieFonctionPublique.non_concerne
    entity = Individu
    definition_period = MONTH
    label = "Categorie de l'emploi dans la fonction publique territoriale"


class TypeFonctionPublique(Enum):
    __order__ = "etat territoriale non_concerne"
    etat = "État"
    territoriale = "Territoriale"
    non_concerne = "Non concerné"


class type_fonction_publique(__ForwardVariable):
    value_type = Enum
    possible_values = TypeFonctionPublique
    default_value = TypeFonctionPublique.non_concerne
    entity = Individu
    definition_period = MONTH
    label = "Type de l'emploi dans la fonction publique"


class employeur_public_direction(__ForwardVariable):
    value_type = str
    entity = Individu
    definition_period = MONTH
    label = "Identifiant de la direction au sein de l'employeur public"


class employeur_public(__ForwardVariable):
    value_type = str
    entity = Individu
    definition_period = MONTH
    label = "Identifiant de l'employeur public"


class employeur_public_fonction(__ForwardVariable):
    value_type = str
    entity = Individu
    definition_period = MONTH
    label = "Code fonction dans la fonction publique"


class employeur_public_echelle(Variable):
    value_type = str
    entity = Individu
    definition_period = MONTH
    label = "Code échelle dans la fonction publique"

    def formula(individu, period, parameters):
        echelon = individu("echelon", period)
        return (
            parameters(period)
            .marche_travail.remuneration_fonction_publique.echelons.meta[echelon]
            .echelle
        )


class ZoneTravailFonctionPublique(Enum):
    __order__ = "brousse noumea non_concerne"
    brousse = "Brousse"
    noumea = "Nouméa"
    non_concerne = "Non concerné"


class zone_travail_fonction_publique(__ForwardVariable):
    value_type = Enum
    possible_values = ZoneTravailFonctionPublique
    default_value = ZoneTravailFonctionPublique.non_concerne
    entity = Individu
    label = "Lieu de travail pour le calcul du taux d'indexation"
    definition_period = MONTH


class taux_indexation_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Taux d'indexation pour la rémunération dans le secteur public"
    definition_period = MONTH

    def formula(individu, period, parameters):
        lieu = individu("zone_travail_fonction_publique", period)
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.taux_indexation[lieu]


class temps_de_travail(__ForwardVariable):
    value_type = float
    entity = Individu
    label = "Temps de travail"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH
    default_value = 1.0


class est_retraite(Variable):
    value_type = bool
    entity = Individu
    label = "Personne retraitée"
    definition_period = MONTH

    def formula(individu, period, parameters):
        age_en_mois = individu("age_en_mois", period)
        age_max = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.mois_retraite
        return age_en_mois >= age_max


class valeur_point(Variable):
    value_type = float
    entity = Individu
    label = "Valeur du point dans la fonction publique"
    definition_period = MONTH

    def formula(individu, period, parameters):
        type_fonction_publique = individu("type_fonction_publique", period)
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.valeur_point[
            type_fonction_publique
        ]


class traitement_brut(Variable):
    value_type = float
    entity = Individu
    label = "Traitement brut"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period):
        indice = individu("indice_fonction_publique_paie", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)

        ajustement = individu("traitement_brut_ajustement", period)

        est_retraite = individu("est_retraite", period)

        return not_(est_retraite) * (
            indice * valeur_point * temps_de_travail + ajustement
        )


class traitement_brut_ajustement(Variable):
    value_type = float
    entity = Individu
    label = "Ajustement au traitement brut"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"


class complement_brut(Variable):
    value_type = float
    entity = Individu
    label = "Ressources brutes complémentaires"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"


class allocations_familiales_publiques(Variable):
    value_type = float
    entity = Individu
    label = "Ressources brutes complémentaires"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"


class traitement_complement_indexation(Variable):
    value_type = float
    entity = Individu
    label = "Indexation du traitement"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        P = parameters(period).marche_travail.remuneration_fonction_publique
        taux_equilibre = P.taux_equilibre

        traitement_brut = individu("traitement_brut", period)
        return (
            traitement_brut
            * (1 - taux_equilibre)
            * (taux_indexation_fonction_publique - 1)
        )


class indemnite_residence(Variable):
    value_type = float
    entity = Individu
    label = "Indemnité de résidence dans le secteur public"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        indice = individu("indice_fonction_publique_paie", period)
        temps_de_travail = individu("temps_de_travail", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        valeur_point = individu("valeur_point", period)
        est_retraite = individu("est_retraite", period)

        taux = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.indemnite_residence.taux

        return not_(est_retraite) * (
            indice
            * valeur_point
            * temps_de_travail
            * taux_indexation_fonction_publique
            * taux
        )


class base_cotisation_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = (
        "Base de rémunération de la fonction publique pour le calcul des cotisations"
    )
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period):
        traitement_brut = individu("traitement_brut", period)
        traitement_complement_indexation = individu(
            "traitement_complement_indexation", period
        )
        indemnite_residence = individu("indemnite_residence", period)
        primes_fonction_publique = individu("primes_fonction_publique", period)
        complement_brut = individu("complement_brut", period)

        est_retraite = individu("est_retraite", period)

        return not_(est_retraite) * (
            traitement_brut
            + traitement_complement_indexation
            + indemnite_residence
            + primes_fonction_publique
            + complement_brut
        )


class cotisation_RUAMM_ajustement(Variable):
    value_type = float
    entity = Individu
    label = "Coefficient d'ajustement au temps de travail pour le calcul des cotisations RUAMM"
    definition_period = MONTH

    def formula(individu, period):
        temps_de_travail = individu("temps_de_travail", period)
        return where(temps_de_travail < 0.8, temps_de_travail, 1)


class cotisation_RUAMMS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée RUAMM"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).marche_travail.remuneration_fonction_publique.ruamm

        ajustement = individu("cotisation_RUAMM_ajustement", period)
        not_nul_ajustement = where(ajustement == 0, 1, ajustement)
        return -P.bareme_salarie.calc(base / not_nul_ajustement) * ajustement


class cotisation_RUAMMP(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation patronale RUAMM"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).marche_travail.remuneration_fonction_publique.ruamm
        ajustement = individu("cotisation_RUAMM_ajustement", period)
        not_nul_ajustement = where(ajustement == 0, 1, ajustement)
        return P.bareme_patronale.calc(base / not_nul_ajustement) * ajustement


class cotisation_MCS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée MCS"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).marche_travail.remuneration_fonction_publique.mcs
        return -P.taux_salarie * base


class cotisation_NMF_taux_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Taux de cotisation salariée NMF"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.nmf.taux_salarie


class cotisation_NMFS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée NMF"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period):
        taux = individu("cotisation_NMF_taux_salarie", period)
        base = individu("base_cotisation_fonction_publique", period)
        return -taux * base


class cotisation_NMF_taux_patronale(Variable):
    value_type = float
    entity = Individu
    label = "Taux de cotisation patronale NMF"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.nmf.taux_patronale


class cotisation_NMFP(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation patronale NMF"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period):
        taux = individu("cotisation_NMF_taux_patronale", period)
        base = individu("base_cotisation_fonction_publique", period)
        return taux * base


class base_cotisation_NCJ(Variable):
    value_type = float
    entity = Individu
    label = "Base pour les cotisations NCJ"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        indice = individu("indice_fonction_publique", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = individu("valeur_point", period)

        taux_majoration = parameters(
            period
        ).marche_travail.remuneration_fonction_publique.ncj.taux_majoration

        return indice * valeur_point * temps_de_travail * (1 + taux_majoration)


class cotisation_NCJS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée NCJ"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_NCJ", period)

        P = parameters(period).marche_travail.remuneration_fonction_publique.ncj
        return -P.taux_salarie * base


class cotisation_NCJP(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation patronale NCJ"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_NCJ", period)

        P = parameters(period).marche_travail.remuneration_fonction_publique.ncj
        return P.taux_patronale * base
