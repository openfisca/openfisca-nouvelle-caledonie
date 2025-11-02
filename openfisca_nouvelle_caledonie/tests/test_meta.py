"""Ajoute des tests directement en python."""

from openfisca_nouvelle_caledonie import CountryTaxBenefitSystem


def test_metadata():
    """Vérifie la bonne mise à jour des métadonnées du dépôt."""
    tbs = CountryTaxBenefitSystem()
    metadata = tbs.get_package_metadata()
    assert metadata["name"] == "openfisca-nouvelle-caledonie"
    assert (
        metadata["repository_url"]
        == "https://github.com/openfisca/openfisca-nouvelle-caledonie"
    )
