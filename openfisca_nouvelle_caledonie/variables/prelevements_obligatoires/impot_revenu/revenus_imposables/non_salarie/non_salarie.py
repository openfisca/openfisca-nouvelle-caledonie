"""Revenus des non-salariés."""

from openfisca_core.model_api import YEAR, Variable, max_
from openfisca_nouvelle_caledonie.entities import FoyerFiscal


class revenu_categoriel_non_salarie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Revenus catégoriels non salariés"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return max_(
            foyer_fiscal("bic", period)
            + foyer_fiscal("ba", period)
            + foyer_fiscal("bnc", period),
            0,
        )
