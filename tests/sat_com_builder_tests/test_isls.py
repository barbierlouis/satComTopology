from sat_com_builder.links import (
    inter_satellite_link_generator,
)
from sat_com_model.models import InterSatelliteLinkDirection
import pytest
from math import floor

class TestIsls:
    '''
    This class verifies that the ISL Grid+ configuration is properly defined.
    All the hereafter commented code is the reference code from the hypatia function test_isls.py, which has
    been adapted to satComTopology
    '''

    '''
    def test_isls_empty(self):
        satgen.generate_empty_isls("isls_empty.txt.tmp")
        isls_list = satgen.read_isls("isls_empty.txt.tmp", 0)
        self.assertEqual(0, len(isls_list))
        os.remove("isls_empty.txt.tmp")
    '''

    def test_isls_plus_grid(self):
        for values in [(25, 25, 1), (10, 5, 0), (24, 66, 6), (3, 3, 0)]:
            number_orbits = values[0]
            number_satellites_per_orbit = values[1]
            isl_shift = values[2]
            # satgen.generate_plus_grid_isls("isls.txt.tmp", number_orbits, number_satellites_per_orbit, isl_shift)
            # isls_list = satgen.read_isls("isls.txt.tmp", number_orbits * number_satellites_per_orbit)
            isls_list = inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(number_orbits, number_satellites_per_orbit, isl_shift, idx_offset=0)
            # os.remove("isls.txt.tmp")
            # self.assertEqual(len(isls_list), number_orbits * number_satellites_per_orbit * 2)
            assert len(isls_list) == number_orbits * number_satellites_per_orbit * 2
            # self.assertEqual(len(set(isls_list)), number_orbits * number_satellites_per_orbit * 2)
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
                # self.assertTrue((min(i, neighbor_1), max(i, neighbor_1)) in isls_list)
                assert (min(i, neighbor_1), max(i, neighbor_1), InterSatelliteLinkDirection.ORBITAL) in isls_list
                # self.assertTrue((min(i, neighbor_2), max(i, neighbor_2)) in isls_list)
                assert (min(i, neighbor_2), max(i, neighbor_2), InterSatelliteLinkDirection.ORBITAL) in isls_list
                # self.assertTrue((min(i, neighbor_3), max(i, neighbor_3)) in isls_list)
                assert (min(i, neighbor_3), max(i, neighbor_3), InterSatelliteLinkDirection.ADJACENT) in isls_list
                # self.assertTrue((min(i, neighbor_4), max(i, neighbor_4)) in isls_list)
                assert (min(i, neighbor_4), max(i, neighbor_4), InterSatelliteLinkDirection.ADJACENT) in isls_list

    def test_isls_plus_grid_invalid(self):
        with pytest.raises(ValueError):
            inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(2, 2, 0, idx_offset=0)

        '''try:
            satgen.generate_plus_grid_isls("isls.txt.tmp", 2, 2, 0)
            self.fail()
        except ValueError:
            self.assertTrue(True) '''

        with pytest.raises(ValueError):
            inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(3, 2, 0, idx_offset=0)

        '''try:
            satgen.generate_plus_grid_isls("isls.txt.tmp", 3, 2, 0)
            self.fail()
        except ValueError:
            self.assertTrue(True)'''

        with pytest.raises(ValueError):
            inter_satellite_link_generator.generate_inter_satellite_links_grid_from_two_line_element_file(1, 1, 0, idx_offset=0)

        '''try:
            satgen.generate_plus_grid_isls("isls.txt.tmp", 1, 1, 0)
            self.fail()
        except ValueError:
            self.assertTrue(True)'''

'''
    def test_isls_invalid_file(self):
        local_shell = exputil.LocalShell()

        # Invalid left index
        local_shell.write_file(
            "isls.txt.tmp",
            "2 3\n5 6\n9 0"
        )
        try:
            satgen.read_isls("isls.txt.tmp", 9)
            self.fail()
        except ValueError:
            self.assertTrue(True)
        os.remove("isls.txt.tmp")

        # Invalid right index
        local_shell.write_file(
            "isls.txt.tmp",
            "2 3\n5 6\n6 9\n3 99"
        )
        try:
            satgen.read_isls("isls.txt.tmp", 50)
            self.fail()
        except ValueError:
            self.assertTrue(True)
        os.remove("isls.txt.tmp")

        # Invalid left index
        local_shell.write_file(
            "isls.txt.tmp",
            "2 3\n5 6\n6 8\n-3 3"
        )
        try:
            satgen.read_isls("isls.txt.tmp", 50)
            self.fail()
        except ValueError:
            self.assertTrue(True)
        os.remove("isls.txt.tmp")

        # Invalid right index
        local_shell.write_file(
            "isls.txt.tmp",
            "2 3\n5 6\n1 -3\n6 8"
        )
        try:
            satgen.read_isls("isls.txt.tmp", 50)
            self.fail()
        except ValueError:
            self.assertTrue(True)
        os.remove("isls.txt.tmp")

        # Left is larger than right
        local_shell.write_file(
            "isls.txt.tmp",
            "6 5"
        )
        try:
            satgen.read_isls("isls.txt.tmp", 10)
            self.fail()
        except ValueError:
            self.assertTrue(True)
        os.remove("isls.txt.tmp")

        # Left is equal to right
        local_shell.write_file(
            "isls.txt.tmp",
            "5 5"
        )
        try:
            satgen.read_isls("isls.txt.tmp", 10)
            self.fail()
        except ValueError:
            self.assertTrue(True)
        os.remove("isls.txt.tmp")

        # Duplicate
        local_shell.write_file(
            "isls.txt.tmp",
            "2 3\n5 6\n3 9\n5 6\n2 9"
        )
        try:
            satgen.read_isls("isls.txt.tmp", 10)
            self.fail()
        except ValueError:
            self.assertTrue(True)
        os.remove("isls.txt.tmp")

        '''

# if __name__ == '__main__':
#     unittest.main()