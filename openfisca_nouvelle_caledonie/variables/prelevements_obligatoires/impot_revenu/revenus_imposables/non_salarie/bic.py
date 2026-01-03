"""Bénéfices industriels et commerciaux (BIC)."""

from openfisca_core.model_api import YEAR, Variable, max_
from openfisca_nouvelle_caledonie.entities import FoyerFiscal, Individu
from openfisca_nouvelle_caledonie.variables.prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie import (
    benefices_apres_imputations_deficits,
)


class bic_vente_fabrication_transformation_ca_ht(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "EA",
        1: "EB",
        2: "EC",
    }
    entity = Individu
    label = "Activités de ventes, fabrication, transformation : chiffre d’affaires hors taxes"
    definition_period = YEAR


class bic_vente_fabrication_transformation_achats(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "ED",
        1: "EE",
        2: "EF",
    }
    entity = Individu
    label = "Activités de ventes, fabrication, transformation : achats"
    definition_period = YEAR


class bic_vente_fabrication_transformation_salaires_et_sous_traitance(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "EG",
        1: "EH",
        2: "EI",
    }
    entity = Individu
    label = "Activités de ventes, fabrication, transformation : saalires nets versés et sous traitance"
    definition_period = YEAR


class bic_services_ca_ht(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "FA",
        1: "FB",
        2: "FC",
    }
    entity = Individu
    label = "Activités de ventes, fabrication, transformation : chiffre d’affaires hors taxes"
    definition_period = YEAR


class bic_services_achats(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "FD",
        1: "FE",
        2: "FF",
    }
    entity = Individu
    label = "Activités de ventes, fabrication, transformation : achats"
    definition_period = YEAR


class bic_services_salaires_et_sous_traitance(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "FG",
        1: "FH",
        2: "FI",
    }
    entity = Individu
    label = "Activités de ventes, fabrication, transformation : saalires nets versés et sous traitance"
    definition_period = YEAR


class bic_forfait_vente_individuel(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices indutriels et commerciaux au forfait - activités de vente (individuel)"
    definition_period = YEAR

    def formula(individu, period, parameters):
        abattement = parameters(
            period
        ).prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie.bic.abattement

        return abattement * (
            individu("bic_vente_fabrication_transformation_ca_ht", period)
            - individu("bic_vente_fabrication_transformation_achats", period)
            - individu(
                "bic_vente_fabrication_transformation_salaires_et_sous_traitance",
                period,
            )
        )


class bic_forfait_services_individuel(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices indutriels et commerciaux au forfait - activités de services (individuel)"
    definition_period = YEAR

    def formula(individu, period, parameters):
        abattement = parameters(
            period
        ).prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie.bic.abattement

        return abattement * (
            individu("bic_services_ca_ht", period)
            - individu("bic_services_achats", period)
            - individu("bic_services_salaires_et_sous_traitance", period)
        )


# Régime réel simplifié (Cadre 10 de la déclaration complémentaire)


class benefices_industriels_et_commerciaux_reel_simplifie(Variable):
    unit = "currency"
    cerfa_field = {
        0: "IA",
        1: "IB",
    }
    value_type = float
    entity = Individu
    label = "Bénéfices indutriels et commerciaux au régime réel simplifié"
    definition_period = YEAR


class deficits_industriels_et_commerciaux_reel_simplifie(Variable):
    unit = "currency"
    cerfa_field = {
        0: "ID",
        1: "IE",
    }
    value_type = float
    entity = Individu
    label = "Déficits indutriels et commerciaux au régime réel simplifié"
    definition_period = YEAR


# Régime réel normal (Cadre 10 de la déclaration complémentaire)


class benefices_industriels_et_commerciaux_reel_normal(Variable):
    unit = "currency"
    cerfa_field = {
        0: "LA",
        1: "LB",
    }
    value_type = float
    entity = Individu
    label = "Bénéfices indutriels et commerciaux au régime réel normal"
    definition_period = YEAR


class deficits_industriels_et_commerciaux_reel_normal(Variable):
    unit = "currency"
    cerfa_field = {
        0: "LJ",
        1: "LK",
    }
    value_type = float
    entity = Individu
    label = "Déficits indutriels et commerciaux au régime réel normal"
    definition_period = YEAR


class bic_individuel(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices indutriels et commerciaux au réel (individuel)"
    definition_period = YEAR

    def formula(individu, period):
        return (
            individu("bic_forfait_individuel_net_de_cotisations", period)
            + individu("benefices_industriels_et_commerciaux_reel_simplifie", period)
            + individu("benefices_industriels_et_commerciaux_reel_normal", period)
        )


class deficits_industriels_et_commerciaux_reels(Variable):
    unit = "currency"
    value_type = float
    entity = FoyerFiscal
    label = "Bénéfices indutriels et commerciaux au réel (individuel)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return foyer_fiscal.sum(
            foyer_fiscal.members(
                "deficits_industriels_et_commerciaux_reel_simplifie", period
            )
            + foyer_fiscal.members(
                "deficits_industriels_et_commerciaux_reel_normal", period
            )
        )


class bic_individuel_apres_imputaion_deficits(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices indutriels et commerciaux individuels"
    definition_period = YEAR

    def formula(individu, period):
        return benefices_apres_imputations_deficits(
            individu,
            "bic_individuel",
            "deficits_industriels_et_commerciaux_reels",
            period,
        )


class bic_forfait_individuel(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Bénéfices indutriels et commerciaux au forfait (individuel)"
    definition_period = YEAR

    def formula(individu, period):
        bic_vente = max_(
            individu("bic_forfait_vente_individuel", period),
            0,
        )
        bic_services = max_(
            individu("bic_forfait_services_individuel", period),
            0,
        )
        return bic_vente + bic_services


class bic_forfait_individuel_net_de_cotisations(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = (
        "Bénéfices indutriels et commerciaux au forfait (individuel) net de cotisations"
    )
    definition_period = YEAR

    def formula(individu, period):
        return max_(
            (
                individu("bic_forfait_individuel", period)
                - individu("cotisations_non_salarie", period)
            ),
            0,
        )


class bic(Variable):
    unit = "currency"
    value_type = float
    entity = FoyerFiscal
    label = "Bénéfices indutriels et commerciaux"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return foyer_fiscal.sum(
            foyer_fiscal.members("bic_individuel_apres_imputaion_deficits", period)
        )
