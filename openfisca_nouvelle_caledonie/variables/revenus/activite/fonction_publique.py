from openfisca_core.indexed_enums import Enum
from openfisca_core.model_api import *
from openfisca_nouvelle_caledonie.entities import Individu


class CategorieFonctionPubliqueTerritoriale(Enum):
    __order__ = " categorie_a categorie_b categorie_c non_concerne"
    categorie_a = "Categorie A"
    categorie_b = "Categorie B"
    categorie_c = "Categorie C"
    non_concerne = "Non concerné"


class categorie_fonction_publique_territoriale(Variable):
    value_type = Enum
    possible_values = CategorieFonctionPubliqueTerritoriale
    default_value = CategorieFonctionPubliqueTerritoriale.non_concerne
    entity = Individu
    definition_period = MONTH
    label = "Categorie de l'emploi dans la fonction publique territoriale"


class indice_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Indice de rémunération pour le secteur public"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class taux_indexation_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Taux d'indexation pour la rémunération dans le secteur public"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH


class temps_de_travail(Variable):
    value_type = float
    entity = Individu
    label = "Temps de travail"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH
    default_value = 0.1


class temps_de_travail(Variable):
    value_type = float
    entity = Individu
    label = "Temps de travail"
    set_input = set_input_dispatch_by_period
    definition_period = MONTH
    default_value = 0.1


class traitement_brut(Variable):
    value_type = float
    entity = Individu
    label = "Traitement brut"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        indice = individu("indice_fonction_publique", period)
        temps_de_travail = individu("temps_de_travail", period)
        valeur_point = parameters(period).remuneration_fonction_publique.valeur_point

        return indice * valeur_point * temps_de_travail


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
        P = parameters(period).remuneration_fonction_publique
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
        indice = individu("indice_fonction_publique", period)
        temps_de_travail = individu("temps_de_travail", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        valeur_point = parameters(period).remuneration_fonction_publique.valeur_point

        return (
            indice
            * valeur_point
            * temps_de_travail
            * taux_indexation_fonction_publique
            * 0.03
        )


class prime_fonction_publique(Variable):
    value_type = float
    entity = Individu
    label = "Prime pour catégorie A dans le secteur public"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        cat = individu("categorie_fonction_publique_territoriale", period)
        prime = parameters(period).remuneration_fonction_publique.prime[cat]

        temps_de_travail = individu("temps_de_travail", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        valeur_point = parameters(period).remuneration_fonction_publique.valeur_point

        return (
            prime * valeur_point * temps_de_travail * taux_indexation_fonction_publique
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
        prime_fonction_publique = individu("prime_fonction_publique", period)
        return (
            traitement_brut
            + traitement_complement_indexation
            + indemnite_residence
            + prime_fonction_publique
        )


class cotisation_RUAMMS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée RUAMM"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).remuneration_fonction_publique.ruamm
        return -P.bareme_salarie.calc(base)


class cotisation_RUAMMP(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation patronale RUAMM"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).remuneration_fonction_publique.ruamm
        return P.bareme_patronale.calc(base)


class cotisation_MCS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée MCS"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).remuneration_fonction_publique.mcs
        return -P.taux_salarie * base


class cotisation_NMFS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée NMF"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).remuneration_fonction_publique.nmf
        return -P.taux_salarie * base


class cotisation_NMFP(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation patronale NMF"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        base = individu("base_cotisation_fonction_publique", period)
        P = parameters(period).remuneration_fonction_publique.nmf
        return P.taux_patronale * base


class cotisation_NCJS(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation salariée NCJ"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        traitement_brut = individu("traitement_brut", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        base = traitement_brut * taux_indexation_fonction_publique

        P = parameters(period).remuneration_fonction_publique.ncj
        return -P.taux_salarie * base


class cotisation_NCJP(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation patronale NCJ"
    set_input = set_input_divide_by_period
    definition_period = MONTH
    unit = "currency"

    def formula(individu, period, parameters):
        traitement_brut = individu("traitement_brut", period)
        taux_indexation_fonction_publique = individu(
            "taux_indexation_fonction_publique", period
        )
        base = traitement_brut * taux_indexation_fonction_publique

        P = parameters(period).remuneration_fonction_publique.ncj
        return P.taux_patronale * base
