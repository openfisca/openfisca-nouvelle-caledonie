"""Pensions."""

from openfisca_core.model_api import YEAR, Variable, max_, min_, where
from openfisca_nouvelle_caledonie.entities import FoyerFiscal, Individu

# PENSIONS, RETRAITES ET RENTES À TITRE GRATUIT

# Déclarez lignes PA à PC les sommes perçues en 2024 par chaque membre du
# foyer, notamment :
# - le total net annuel des pensions perçues au titre des retraites publiques ou privées
# territoriales ou étrangères ;
# - les rentes et pensions d’invalidité imposables, servies par les organismes de sé-
# curité sociale ;
# - les rentes viagères à titre gratuit ;
# - les pensions alimentaires ;
# - les rentes versées à titre de prestation compensatoire en cas de divorce (voir
# dépliant d’information pour modalités) ;
# - la contribution aux charges du mariage lorsque son versement résulte d’une dé-
# cision de justice.
# Elles bénéficient d’un abattement de 10 %, plafonné à 550 000 F, qui sera calculé
# automatiquement. Les pensions de source métropolitaine sont exclusivement impo-
# sables en Nouvelle-Calédonie pour les résidents du territoire.
# Sommes à ne pas déclarer :
# - les prestations familiales légales (allocations familiales et complément familial,
# allocations prénatales et de maternité, indemnités en faveur des femmes en
# couches…) ;
# - les salaires perçus dans le cadre d’un contrat d’apprentissage ou d’un contrat
# unique d’alternance ;
# - les salaires perçus dans le cadre du volontariat civil à l’aide technique (VCAT) ;
# - les allocations de chômage en cas de perte d’emploi ;
# - les indemni


class pension_retraite_rente_imposables(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "PA",
        1: "PB",
        2: "PC",
    }
    entity = Individu
    label = "Pensions, retraites et rentes au sens strict imposables (rentes à titre onéreux exclues)"
    definition_period = YEAR


class pension_retraite_rente_imposables_rectifiees(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "PP",
        1: "PQ",
        2: "PR",
    }
    entity = Individu
    label = "Pensions, retraites et rentes au sens strict imposables (rentes à titre onéreux exclues)"
    definition_period = YEAR


class pension_imposable_apres_deduction_et_abattement(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Pensions imposables après déduction et abattement"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        tspr = parameters(
            period
        ).prelevements_obligatoires.impot_revenu.revenus_imposables.tspr

        deduction_pension = tspr.deduction_pension

        # Calcul par individu (comme dans le code Java)
        # Pensions non rectifiées (PA/PB/PC) et rectifiées (PP/PQ/PR) par individu
        pension_non_rectifiee = foyer_fiscal.members(
            "pension_retraite_rente_imposables", period
        )
        pension_rectifiee = foyer_fiscal.members(
            "pension_retraite_rente_imposables_rectifiees", period
        )
        pension_totale_individu = pension_non_rectifiee + pension_rectifiee

        # DeductionsPensionsRule2008: déduction 10% sur le total (PA+PP) par individu (plafond 550k par individu)
        deduction_10_totale_individu = min_(
            pension_totale_individu * deduction_pension.taux, deduction_pension.plafond
        )

        # DeductionPensionsRectifieRule2008: déduction 10% sur la partie non rectifiée (PA) par individu (plafond 550k par individu)
        deduction_10_non_rectifiee_individu = min_(
            pension_non_rectifiee * deduction_pension.taux, deduction_pension.plafond
        )

        # AbattementPensionsRule2008: abattement 20% sur (PA - deduction_10_sur_PA) par individu (plafond 1800k par individu)
        pension_non_rectifiee_apres_deduction_10_individu = max_(
            pension_non_rectifiee - deduction_10_non_rectifiee_individu, 0
        )
        abattement_individu = min_(
            pension_non_rectifiee_apres_deduction_10_individu * tspr.abattement.taux,
            tspr.abattement.plafond,
        )

        # PensionsRule2008: pension = pension_totale - deduction_10_totale - abattement_20
        pension_apres_abattement_individu = max_(
            pension_totale_individu
            - deduction_10_totale_individu
            - abattement_individu,
            0,
        )

        # Total au niveau du foyer fiscal
        pension_apres_abattement = foyer_fiscal.sum(pension_apres_abattement_individu)

        # Abattement spécial sur les pensions pour les non-résidents
        pension_totale_apres_deduction = foyer_fiscal.sum(
            max_(pension_totale_individu - deduction_10_totale_individu, 0)
        )
        abattement_total = foyer_fiscal.sum(abattement_individu)
        pension_imposable_totale = foyer_fiscal.sum(pension_totale_individu)

        pension_apres_abattements_non_resident = max_(
            pension_totale_apres_deduction
            - abattement_total
            - min_(
                pension_imposable_totale, deduction_pension.plafond_non_resident
            ),  # Abattement spécial non résident
            0,
        )
        return where(
            foyer_fiscal("resident", period),
            pension_apres_abattement,
            pension_apres_abattements_non_resident,
        )


# Revenus de la déclaration complémentaire

# Revenus différés salaires et pensions (Cadre 9)


class pensions_imposees_selon_le_quotient(Variable):
    unit = "currency"
    value_type = float
    cerfa_field = {
        0: "PD",
        1: "PE",
    }
    entity = Individu
    label = "Pensions imposées selon le quotient"
    definition_period = YEAR


class annees_de_rappel_pensions(Variable):
    value_type = int
    cerfa_field = {
        0: "PG",
        1: "PH",
        2: "PI",
    }
    entity = Individu
    label = "Années de rappel pour les salaires pensions selon le quotient"
    definition_period = YEAR


class pensions_differes_apres_deduction(Variable):
    unit = "currency"
    value_type = float
    entity = Individu
    label = "Pensions différées après déduction et abattement"
    definition_period = YEAR

    def formula(individu, period, parameters):
        tspr = parameters(
            period
        ).prelevements_obligatoires.impot_revenu.revenus_imposables.tspr

        pension_imposable = individu("pensions_imposees_selon_le_quotient", period)

        deduction_pension = tspr.deduction_pension
        montant_deduction_pension = min_(
            pension_imposable * deduction_pension.taux,
            deduction_pension.plafond,
        )
        pension_apres_deduction = max_(pension_imposable - montant_deduction_pension, 0)
        abatemment = min_(
            pension_apres_deduction * tspr.abattement.taux, tspr.abattement.plafond
        )
        annees_de_rappel_pensions = individu("annees_de_rappel_pensions", period)

        pension_apres_abattement = max_(pension_apres_deduction - abatemment, 0)

        # Abattement spécial sur les pensions pour les non-résidents

        pension_apres_abattements_non_resident = max_(
            (
                pension_apres_deduction
                - abatemment
                - min_(
                    pension_imposable, deduction_pension.plafond_non_resident
                )  # Abattement spécial non résident
            ),
            0,
        )

        return where(
            annees_de_rappel_pensions > 0,
            where(
                individu.foyer_fiscal("resident", period),
                pension_apres_abattement,
                pension_apres_abattements_non_resident,
            )
            / (annees_de_rappel_pensions + (annees_de_rappel_pensions == 0)),
            0,
        )
