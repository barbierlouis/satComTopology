from sat_com_builder.links import (
    inter_satellite_link_generator,
)
from sat_com_model.models import InterSatelliteLinkDirection
import pytest
from math import floor

class TestIsls:
    '''
    This class verifies that the ISL Grid+ configuration is properly defined.
    All the hereafter commented code is inspired from the hypatia function test_isls.py, which has
    been adapted to satComTopology
    '''

    def test_isls_plus_grid(self):
        for values in [(25, 25, 1), (10, 5, 0), (24, 66, 6), (3, 3, 0)]:
            number_orbits = values[0]
            number_satellites_per_orbit = values[1]
            isl_shift = values[2]
            isls_list = inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(number_orbits, number_satellites_per_orbit, isl_shift, idx_offset=0)
            assert len(isls_list) == number_orbits * number_satellites_per_orbit * 2
            assert len(set(isls_list)) == number_orbits * number_satellites_per_orbit * 2
            for i in range(number_orbits * number_satellites_per_orbit):
                orbit_of_i = int(floor(i / float(number_satellites_per_orbit)))

                # Links in same orbit
                neighbor_1 = orbit_of_i * number_satellites_per_orbit + (i + number_satellites_per_orbit + 1) % number_satellites_per_orbit
                neighbor_2 = orbit_of_i * number_satellites_per_orbit + (i + number_satellites_per_orbit - 1) % number_satellites_per_orbit

                # Links to different orbits
                neighbor_3 = (
                    ((orbit_of_i + number_orbits - 1) % number_orbits)
                    * number_satellites_per_orbit + (i + number_satellites_per_orbit - isl_shift) % number_satellites_per_orbit
                )
                neighbor_4 = (
                    ((orbit_of_i + number_orbits + 1) % number_orbits)
                    * number_satellites_per_orbit + (i + number_satellites_per_orbit + isl_shift) % number_satellites_per_orbit
                )

                # All of them must be present
                assert (min(i, neighbor_1), max(i, neighbor_1), InterSatelliteLinkDirection.ORBITAL) in isls_list
                assert (min(i, neighbor_2), max(i, neighbor_2), InterSatelliteLinkDirection.ORBITAL) in isls_list
                assert (min(i, neighbor_3), max(i, neighbor_3), InterSatelliteLinkDirection.ADJACENT) in isls_list
                assert (min(i, neighbor_4), max(i, neighbor_4), InterSatelliteLinkDirection.ADJACENT) in isls_list

    def test_isls_plus_grid_invalid(self):
        with pytest.raises(ValueError):
            inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(2, 2, 0, idx_offset=0)

        with pytest.raises(ValueError):
            inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(3, 2, 0, idx_offset=0)

        with pytest.raises(ValueError):
            inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(1, 1, 0, idx_offset=0)
