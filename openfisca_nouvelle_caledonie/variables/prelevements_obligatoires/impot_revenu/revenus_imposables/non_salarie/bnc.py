"""Bénéfices non commerciaux (BNC)."""

from openfisca_core.model_api import YEAR, Variable, max_, min_
from openfisca_nouvelle_caledonie.entities import FoyerFiscal, Individu
from openfisca_nouvelle_caledonie.variables.prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie import (
    benefices_apres_imputations_deficits,
    get_multiple_and_plafond_cafat_cotisation,
)


class bnc_recettes_ht(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "HA",
        1: "HB",
        2: "HC",
    }
    entity = Individu
    label = "Recettes annuelles des bénéfices non-commerciaux"
    definition_period = YEAR


# Régime réel simplifié (Cadre 10 de la déclaration complémentaire)


class benefices_non_commerciaux_reel_simplifie(Variable):
    unit = "currency"
    cerfa_field = {
        0: "KA",
        1: "KB",
    }
    value_type = float
    entity = Individu
    label = "Bénéfices non commerciaux au régime réel simplifié"
    definition_period = YEAR


class deficits_non_commerciaux_reel_simplifie(Variable):
    unit = "currency"
    cerfa_field = {
        0: "KJ",
        1: "KK",
    }
    value_type = float
    entity = Individu
    label = "Déficits non commerciaux au régime réel simplifié"
    definition_period = YEAR


class bnc_forfait_individuel(Variable):
    unit = "currency"
    value_type = float
    label = "Bénéfices non commerciaux au forfait (individuel)"
    entity = Individu
    definition_period = YEAR

    def formula(individu, period, parameters):
        diviseur = parameters(
            period
        ).prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie.bnc.diviseur_recettes
        return individu("bnc_recettes_ht", period) / diviseur  # Forfait


class bnc_forfait_individuel_net_de_cotisations(Variable):
    unit = "currency"
    value_type = float
    label = "Bénéfices non commerciaux au forfait (individuel)"
    entity = Individu
    definition_period = YEAR

    def formula(individu, period, parameters):
        diviseur = parameters(
            period
        ).prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie.bnc.diviseur_recettes
        multiple, plafond_cafat = get_multiple_and_plafond_cafat_cotisation(
            period, parameters
        )
        return max_(
            0,
            individu("bnc_recettes_ht", period) / diviseur  # Forfait
            - min_(
                individu("reste_cotisations_apres_bic_avant_bnc", period),
                multiple * plafond_cafat,
            ),
        )


class bnc_individuel(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices non commerciaux au forfait (individuel)"
    definition_period = YEAR

    def formula(individu, period):
        return individu("bnc_forfait_individuel_net_de_cotisations", period) + individu(
            "benefices_non_commerciaux_reel_simplifie", period
        )


class deficits_non_commerciaux(Variable):
    unit = "currency"
    value_type = float
    entity = FoyerFiscal
    label = "Déficits non commerciaux du foyer fiscal"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return foyer_fiscal.sum(
            foyer_fiscal.members("deficits_non_commerciaux_reel_simplifie", period)
        )


class bnc_individuel_apres_imputaion_deficits(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices non commerciaux individuels après imputation des déficits"
    definition_period = YEAR

    def formula(individu, period):
        return benefices_apres_imputations_deficits(
            individu,
            "bnc_individuel",
            "deficits_non_commerciaux",
            period,
        )


class bnc(Variable):
    unit = "currency"
    value_type = float
    entity = FoyerFiscal
    label = "Bénéfices non commerciaux"
    definition_period = YEAR

    def formula(individu, period):
        return individu.sum(
            individu.members("bnc_individuel_apres_imputaion_deficits", period)
        )
