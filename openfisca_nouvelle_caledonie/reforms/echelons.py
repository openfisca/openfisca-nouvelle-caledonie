"""Réformes pour l'intégration des grilles d'échelons, il sera peut-être pertinent d'intégrer ça au constructeur du TBS."""

import numpy as np

from openfisca_core.model_api import Reform
from openfisca_core.parameters import ParameterNode

period = "2022-12-01"


def build_param(value):
    """Permet la création des feuilles datées dans l'arbre des paramètres."""
    return {"values": {period: value}}


def build_meta_params(name, domaine, echelle, next_name, value):
    """Permet la création des sous-arbres des échelons."""
    next_value = next_name or name
    assert next_value, name
    domaine_value = domaine or "non_concerne"
    return {
        "suivant": build_param(next_value),
        "domaine": build_param(domaine_value),
        "echelle": build_param(echelle),
        "duree_moyenne": build_param(value),
    }


class GrilleReform(Reform):
    def __init__(self, tbs, meta_data, indice_data):
        """Réforme de base pour l'intégration de barèmes par échelon."""
        self.meta_data = meta_data
        self.indice_data = indice_data
        super().__init__(tbs)

    def apply(self):
        def modify_parameters(local_parameters):
            local_parameters.marche_travail.remuneration_fonction_publique.add_child(
                "echelons", ParameterNode("echelons", data={})
            )

            # VIASGRILLES[["Grille indiciaire - Code", "Domaine - code", "Echelle - Code", "Grille Suivante", "Durée Moyenne"]]
            meta_nodes = {
                name: build_meta_params(name, domaine, echelle, next_name, value)
                for [name, domaine, echelle, next_name, value] in self.meta_data
            }
            meta = ParameterNode("meta", data=meta_nodes)
            local_parameters.marche_travail.remuneration_fonction_publique.echelons.add_child(
                "meta", meta
            )

            # VIASGRILLESINM[["Grille", "Inm"]]
            indice_data = {n: build_param(v) for [n, v] in self.indice_data}
            indice = ParameterNode("indice", data=indice_data)
            local_parameters.marche_travail.remuneration_fonction_publique.echelons.add_child(
                "indice", indice
            )

            return local_parameters

        self.modify_parameters(modifier_function=modify_parameters)


class CIReform(GrilleReform):
    def __init__(self, tbs):
        """Réforme pour réaliser les tests en CI."""
        meta_data = [
            ["FTTAE2011", "ER", "", "FTTAE2012", 12],
            ["FTTAE2012", "ER", "", "FTTAE2013", 12],
            ["FTTAE2013", "ER", "", "FTTAE2013", 0],
            ["AG002N009", "ER", "", "AG002N010", 12],
            ["AG002N010", "ER", "", "AG002N011", 12],
            ["AG002N011", "EQ", "", None, np.nan],
            ["YTTAS1006", "ST", "", "YTTAS1007", 12],
            ["Y202 DX0U", None, "D0321P0", "Y202 DX0Z", 12],
        ]

        indice_data = [
            ["FTTAE2011", 401],
            ["FTTAE2012", 402],
            ["FTTAE2013", 403],
            ["AG002N009", 421],
            ["AG002N010", 422],
            ["AG002N011", 423],
        ]
        super().__init__(tbs, meta_data, indice_data)
