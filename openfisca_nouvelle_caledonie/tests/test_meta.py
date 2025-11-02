from .. import CountryTaxBenefitSystem


def test_metadata():
    tbs = CountryTaxBenefitSystem()
    metadata = tbs.get_package_metadata()
    assert metadata["name"] == "openfisca-nouvelle-caledonie"
    assert (
        metadata["repository_url"]
        == "https://github.com/openfisca/openfisca-nouvelle-caledonie"
    )
