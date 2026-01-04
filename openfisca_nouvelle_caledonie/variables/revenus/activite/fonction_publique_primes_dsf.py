"""Primes dans la fonction publique."""

from openfisca_core.model_api import MONTH, Variable
from openfisca_nouvelle_caledonie.entities import Individu


class prime_dsf_fixe_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "prime pour la DSF (et service du contentieux fiscal de la DAJ)"
    reference = "Délib 439 du 30/12/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.dsf.fixe


class prime_dsf_fixe(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "prime pour la DSF (et service du contentieux fiscal de la DAJ)"
    reference = "Délib 439 du 30/12/2008"

    def formula(individu, period):
        direction = individu("employeur_public_direction", period)
        elig = direction == "G1500000"

        montant = individu("prime_dsf_fixe_montant", period)
        temps_de_travail = individu("temps_de_travail", period)
        return elig * montant * temps_de_travail


class prime_dsf_variable_numerateur(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "prime pour la DSF (et service du contentieux fiscal de la DAJ)"
    reference = "Délib 439 du 30/12/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.dsf.variable.numerateur


class prime_dsf_variable_denominateur(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "prime pour la DSF (et service du contentieux fiscal de la DAJ)"
    reference = "Délib 439 du 30/12/2008"

    def formula(individu, period, parameters):
        return parameters(
            period
        ).marche_travail.remuneration_fonction_publique.prime.dsf.variable.denominateur


class prime_dsf_variable(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "prime pour la DSF (et service du contentieux fiscal de la DAJ)"
    reference = "Délib 439 du 30/12/2008"

    def formula(individu, period):
        direction = individu("employeur_public_direction", period)
        elig = direction == "G1500000"

        num = individu("prime_dsf_variable_numerateur", period)
        denom = individu("prime_dsf_variable_denominateur", period)
        montant = (
            individu("traitement_brut", period)
            + individu("traitement_complement_indexation", period)
            + individu("indemnite_residence", period)
        )
        return elig * num / denom * montant
