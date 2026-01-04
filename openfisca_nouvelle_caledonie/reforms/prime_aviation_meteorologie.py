"""Réformes pour l'intégration des valeurs pour la prime dans l'aviation civile et la météorologie. Il sera peut-être pertinent d'intégrer ça au constructeur du TBS."""

from openfisca_core.model_api import Reform
from openfisca_core.parameters import Parameter

period = "2022-12-01"


def build_param(value):
    """Permet la création des feuilles datées dans l'arbre des paramètres."""
    return {"values": {period: value}}


class TableReform(Reform):
    def __init__(self, tbs, data):
        """Réforme de base pour l'intégration de barèmes par échelon."""
        self.data = data
        super().__init__(tbs)

    def apply(self):
        def modify_parameters(local_parameters):
            # [["Echelle", "K_TCH"]]
            for echelle, value in self.data:
                param = Parameter(echelle, data=build_param(value))
                local_parameters.marche_travail.remuneration_fonction_publique.tch.add_child(
                    echelle, param
                )

            return local_parameters

        self.modify_parameters(modifier_function=modify_parameters)


class CIReform(TableReform):
    def __init__(self, tbs):
        """Réforme pour réaliser les tests en CI."""
        data = [["D036 C0", 55501], ["D0321P0", 37397]]
        super().__init__(tbs, data)
