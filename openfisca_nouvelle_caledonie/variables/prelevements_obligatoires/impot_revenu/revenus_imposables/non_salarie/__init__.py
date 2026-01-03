# Helpers


from openfisca_core.model_api import max_, min_, where
from openfisca_nouvelle_caledonie.entities import FoyerFiscal


def get_multiple_and_plafond_cafat_cotisation(period, parameters):
    """Renvoie le multiple et le plafond de la cotisation CAFAT pour l'année revenus donnée."""
    period_plafond = period.start.offset("first-of", "month").offset(11, "month")
    cafat = parameters(
        period_plafond
    ).prelevements_obligatoires.prelevements_sociaux.cafat
    cotisations = parameters(
        period
    ).prelevements_obligatoires.impot_revenu.revenus_imposables.non_salarie.cotisations
    if period_plafond.year >= 2023:
        plafond_cafat = (
            cafat.maladie_retraite.plafond_retraite_mensuel
        )  # Donc année revenus 2023
        multiple = cotisations.plafond_depuis_ir_2024
    else:
        plafond_cafat = cafat.autres_regimes.plafond_mensuel
        multiple = cotisations.plafond_avant_ir_2024

    return multiple, plafond_cafat


def benefices_apres_imputations_deficits(
    individu, benefices_individu_name: str, deficits_foyer_fiscal_name: str, period
):
    """Renvoie les bénéfices après imputation des déficits calculés au niveau du foyer fiscal."""
    deficits = individu.foyer_fiscal(deficits_foyer_fiscal_name, period)
    deficit_impute_declarant = min_(
        deficits,
        individu.foyer_fiscal.declarant_principal(benefices_individu_name, period),
    )

    deficit_impute_conjoint = min_(
        max_(deficits - deficit_impute_declarant, 0),
        individu.foyer_fiscal.conjoint(benefices_individu_name, period),
    )

    deficit_impute_pac = min_(
        max_(deficits - deficit_impute_declarant - deficit_impute_conjoint, 0),
        individu.foyer_fiscal.sum(
            individu.foyer_fiscal.members(benefices_individu_name, period),
            role=FoyerFiscal.ENFANT_A_CHARGE,
        ),
    )
    return where(
        individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL),
        individu(benefices_individu_name, period) - deficit_impute_declarant,
        where(
            individu.has_role(FoyerFiscal.CONJOINT),
            individu(benefices_individu_name, period) - deficit_impute_conjoint,
            individu(benefices_individu_name, period) - deficit_impute_pac,
        ),
    )
