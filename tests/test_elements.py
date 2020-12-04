"""Test suite for ``elements.py``."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu.data
import iniabu.elements


def test_elements_require_parent_class():
    """Test that class requires an appropriate parent class."""
    # Parent class testing
    with pytest.raises(TypeError) as err_info:
        iniabu.elements.Elements(None, None)
    err_msg = err_info.value.args[0]
    assert err_msg == "Elements class must be initialized from IniAbu."


def test_elements_wrong_unit():
    """Raise NotImplementedError if a wrong unit is selected."""
    parent = iniabu.IniAbu()  # fake a correct parent
    unit = "random_unit"
    with pytest.raises(NotImplementedError) as err_info:
        iniabu.elements.Elements(parent, "Si", unit=unit)
    err_msg = err_info.value.args[0]
    assert err_msg == f"The chosen unit {unit} is currently not implemented."


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_elements_eles_list(ini_default, ele1, ele2):
    """Test that the element list is correctly initialized."""
    assert ini_default.element[ele1]._eles == [ele1]
    assert ini_default.element[[ele1, ele2]]._eles == [ele1, ele2]


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_a(ini_default, ele1, ele2):
    """Test isotope atomic number returner."""
    assert (
        ini_default.element[ele1].isotopes_a
        == np.array(iniabu.data.lodders09_elements[ele1][1])
    ).all()

    left = ini_default.element[[ele1, ele2]].isotopes_a
    right = [
        np.array(iniabu.data.lodders09_elements[ele1][1]),
        np.array(iniabu.data.lodders09_elements[ele2][1]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_relative_abundance(ini_default, ele1, ele2):
    """Test isotope relative abundance returner."""
    assert (
        ini_default.element[ele1].isotopes_relative_abundance
        == np.array(iniabu.data.lodders09_elements[ele1][2])
    ).all()

    left = ini_default.element[[ele1, ele2]].isotopes_relative_abundance
    right = [
        np.array(iniabu.data.lodders09_elements[ele1][2]),
        np.array(iniabu.data.lodders09_elements[ele2][2]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_solar_abundance(ini_default, ele1, ele2):
    """Test isotope solar abundance returner."""
    assert (
        ini_default.element[ele1].isotopes_solar_abundance
        == np.array(iniabu.data.lodders09_elements[ele1][3])
    ).all()

    left = ini_default.element[[ele1, ele2]].isotopes_solar_abundance
    right = [
        np.array(iniabu.data.lodders09_elements[ele1][3]),
        np.array(iniabu.data.lodders09_elements[ele2][3]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_solar_abundance_log(ele1, ele2):
    """Test isotope solar abundance returner."""
    ini = iniabu.IniAbu(unit="num_log")
    assert (
        ini.element[ele1].isotopes_solar_abundance
        == np.array(ini.ele_dict_log[ele1][3])
    ).all()

    left = ini.element[[ele1, ele2]].isotopes_solar_abundance
    right = [
        np.array(ini.ele_dict_log[ele1][3]),
        np.array(ini.ele_dict_log[ele2][3]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_solar_abundance_mf(ele1, ele2):
    """Test isotope solar abundance returner."""
    ini = iniabu.IniAbu(unit="mass_fraction")
    assert (
        ini.element[ele1].isotopes_solar_abundance == np.array(ini.ele_dict_mf[ele1][3])
    ).all()

    left = ini.element[[ele1, ele2]].isotopes_solar_abundance
    right = [
        np.array(ini.ele_dict_mf[ele1][3]),
        np.array(ini.ele_dict_mf[ele2][3]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
)
def test_isotopes_solar_abundance_nan(ini_nist, ele1, ele2):
    """Test isotope solar abundance returner when not available."""
    # make sure np.nan is returned for other databases
    assert np.isnan(ini_nist.element[ele1].isotopes_solar_abundance).all()

    val = ini_nist.element[[ele1, ele2]].isotopes_solar_abundance
    assert all([np.isnan(it).all() for it in val])


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_mass(ini_default, ele1, ele2):
    """Query the mass of an element."""
    isos1 = [f"{ele1}-{a}" for a in ini_default.ele_dict[ele1][1]]
    isos_masses1 = np.array([iniabu.data.isotopes_mass[iso] for iso in isos1])
    isos_abus1 = np.array(ini_default.ele_dict[ele1][2])
    mass_expected1 = np.sum(isos_masses1 * isos_abus1)
    assert ini_default.element[ele1].mass == mass_expected1

    isos2 = [f"{ele2}-{a}" for a in ini_default.ele_dict[ele2][1]]
    isos_masses2 = np.array([iniabu.data.isotopes_mass[iso] for iso in isos2])
    isos_abus2 = np.array(ini_default.ele_dict[ele2][2])
    mass_expected2 = np.sum(isos_masses2 * isos_abus2)
    masses_expected = np.array([mass_expected1, mass_expected2])
    masses_gotten = ini_default.element[[ele1, ele2]].mass
    np.testing.assert_equal(masses_gotten, masses_expected)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_solar_abundance(ini_default, ele1, ele2):
    """Test solar abundance property."""
    assert (
        ini_default.element[ele1].solar_abundance
        == iniabu.data.lodders09_elements[ele1][0]
    )
    left = ini_default.element[[ele1, ele2]].solar_abundance
    right = np.array(
        [
            iniabu.data.lodders09_elements[ele1][0],
            iniabu.data.lodders09_elements[ele2][0],
        ]
    )
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
)
def test_solar_abundance_nan(ini_nist, ele1, ele2):
    """Test solar abundance property when not available."""
    assert np.isnan(ini_nist.element[ele1].solar_abundance)
    assert np.isnan(ini_nist.element[[ele1, ele2]].solar_abundance).all()
