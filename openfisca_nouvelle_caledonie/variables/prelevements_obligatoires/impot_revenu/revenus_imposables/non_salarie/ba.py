"""Bénéfices agricoles (BA)."""

from openfisca_core.model_api import YEAR, Variable, max_, min_
from openfisca_nouvelle_caledonie.entities import FoyerFiscal, Individu
from openfisca_nouvelle_caledonie.variables.prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie import (
    benefices_apres_imputations_deficits,
    get_multiple_and_plafond_cafat_cotisation,
)


class chiffre_d_daffaires_agricole_ht_imposable(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "GA",
        1: "GB",
        2: "GC",
    }
    entity = Individu
    label = "Chiffre d’affaires hors taxes tiré des exploitations agricoles imposables"
    definition_period = YEAR
    # Le bénéfice, égal à 1/6 e de ce chiffre d’affaires sera déterminé automatiquement.


class chiffre_d_daffaires_agricole_ht_exonere(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "GD",
        1: "GE",
        2: "GF",
    }
    entity = Individu
    label = "Chiffre d’affaires hors taxes tiré des exploitations agricoles exonérées en vertu d’un bail rural"
    definition_period = YEAR


class benefices_agricoles_regime_forfaitaire(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices agricoles au régime forfaitaire"
    definition_period = YEAR

    def formula(individu, period, parameters):
        # Le bénéfice, égal à 1/6 e de ce chiffre d’affaires sera déterminé automatiquement.
        diviseur = parameters(
            period
        ).prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie.ba.diviseur_ca
        multiple, plafond_cafat = get_multiple_and_plafond_cafat_cotisation(
            period, parameters
        )
        return max_(
            0,
            individu("chiffre_d_daffaires_agricole_ht_imposable", period) / diviseur
            - min_(
                individu("reste_cotisations_apres_bic_bnc_avant_ba", period),
                multiple * plafond_cafat,
            ),
        )


# Régime réel simplifié (Cadre 10 de la déclaration complémentaire)


class benefices_agricoles_regime_reel(Variable):
    unit = "currency"
    cerfa_field = {
        0: "JA",
        1: "JB",
    }
    value_type = float
    entity = Individu
    label = "Bénéfices agricoles du régime réel simplifié"
    definition_period = YEAR


class deficits_agricoles_regime_reel(Variable):
    unit = "currency"
    cerfa_field = {
        0: "JD",
        1: "JE",
    }
    value_type = float
    entity = Individu
    label = "Déficits agricoles du régime réel simplifié"
    definition_period = YEAR


class deficits_agricoles(Variable):
    unit = "currency"
    value_type = float
    entity = FoyerFiscal
    label = "Déficits agricoles du foyer fiscal"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return foyer_fiscal.sum(
            foyer_fiscal.members("deficits_agricoles_regime_reel", period)
        )


class ba_individuel(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices agricoles individuels avant imputation des déficits"
    definition_period = YEAR

    def formula(individu, period):
        return individu("benefices_agricoles_regime_forfaitaire", period) + individu(
            "benefices_agricoles_regime_reel", period
        )


class ba_individuel_apres_imputaion_deficits(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices agricoles individuels après imputation des déficits"
    definition_period = YEAR

    def formula(individu, period):
        return benefices_apres_imputations_deficits(
            individu, "ba_individuel", "deficits_agricoles", period
        )


class ba(Variable):
    """Bénéfices agricoles (BA) imposables."""

    unit = "currency"
    value_type = int
    entity = FoyerFiscal
    label = "Bénéfices agricoles (BA) imposables"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return foyer_fiscal.sum(
            foyer_fiscal.members("ba_individuel_apres_imputaion_deficits", period)
        )
