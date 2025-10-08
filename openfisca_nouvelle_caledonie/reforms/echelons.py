from openfisca_core.model_api import Reform
from openfisca_core.parameters import ParameterNode

period = "2022-12-01"


def build_param(value):
    return {"values": {period: value}}


def build_meta_params(array_string):
    array = array_string.split(",")
    return array[0], {
        "suivant": build_param(array[1]),
        "duree_moyenne": build_param(float(array[2])),
    }


class reform(Reform):
    def __init__(self, tbs):
        super().__init__(tbs)

    def apply(self):
        def modify_parameters(local_parameters):
            local_parameters.remuneration_fonction_publique.add_child(
                "echelons", ParameterNode("echelons", data={})
            )

            # VIASGRILLES[["Grille indiciaire - Code", "Grille Suivante", "Durée Moyenne"]]
            params = """FTTAE2011,FTTAE2012,12
FTTAE2012,FTTAE2013,12
FTTAE2013,FTTAE2013,0
AG002N009,AG002N010,12
AG002N010,AG002N011,12
AG002N011,AG002N010,0""".split("\n")
            meta_items = [build_meta_params(p) for p in params]
            meta_data = {a: b for (a, b) in meta_items}
            meta = ParameterNode("meta", data=meta_data)
            local_parameters.remuneration_fonction_publique.echelons.add_child(
                "meta", meta
            )

            # VIASGRILLESINM[["Grille", "Inm"]]
            indices = {
                "FTTAE2011": 401,
                "FTTAE2012": 402,
                "FTTAE2013": 403,
                "AG002N009": 421,
                "AG002N010": 422,
                "AG002N011": 423,
            }
            indice_data = {i: build_param(indices[i]) for i in indices}
            indice = ParameterNode("indice", data=indice_data)
            local_parameters.remuneration_fonction_publique.echelons.add_child(
                "indice", indice
            )

            return local_parameters

        self.modify_parameters(modifier_function=modify_parameters)
