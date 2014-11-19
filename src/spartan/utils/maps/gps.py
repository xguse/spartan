# gps.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 11/1/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
gps.py
=================================================
Purpose:
Operate on GPS type data.
"""
__author__ = 'Gus Dunn'

from bunch import Bunch

import spartan.utils.errors as e
from spartan.utils.files import tableFile2namedTuple


# ----- Utility functions for this module ----- #
def clean_coord(value):
    if value.upper().startswith('S'):
        return -1 * abs(float(value.strip('S')))

    elif value.upper().startswith('W'):
        return -1 * abs(float(value.strip('W')))

    elif value.upper().startswith('N'):
        return abs(float(value.strip('N')))

    elif value.upper().startswith('E'):
        return abs(float(value.strip('E')))

    else:
        return float(value)




# ----- For Loading GPS info from files ----- #

def load_gps_coords(paths):
    if not isinstance(paths,list):
        paths = [paths]

    gps_files = []
    for path in paths:
        gps_files.append(tableFile2namedTuple(path))

    gps_objs = []
    for coord_group in gps_files:
        for coord in coord_group:
            gps_objs.append(build_GPSCoord(gps_data=coord))

    return GPSCoordTree(gps_coord_objs=gps_objs, level='root')


def build_GPSCoord(gps_data):

    location = gps_data.location
    lat = gps_data.latitude
    lon = gps_data.longitude
    try:
        trace = gps_data.trace
    except AttributeError as exc:
        if "'Table' object has no attribute 'trace'" in exc.message:
            trace = ''
        else:
            raise exc

    trace = '.'.join(['root', trace]).strip('.')

    return GPSCoord(location=location, lat=lat, lon=lon, trace=trace)



class GPSCoordTree(Bunch):
    '''
    Class represents a hierarchical tree of GPSCoord objects grouped by their `trace` strings.
    '''

    def __init__(self, gps_coord_objs=None, level=None, kind='branch', **kwargs):
        '''
        Returns initialized GPS coord tree based on a group of existing `GPSCoord()` objects.


        :param gps_coord_objs:
        :type gps_coord_objs: `list()`
        :param level:
        :param kind:
        :param kwargs:
        :return: GPSCoordTree
        :rtype: `GPSCoordTree()`
        '''

        self.level = level
        self.kind = kind

        super(GPSCoordTree, self).__init__(**kwargs)

        if gps_coord_objs is not None:
            for gps_obj in gps_coord_objs:
                self._grow_branch(gps_obj=gps_obj)




    def _grow_branch(self, gps_obj):
        levels = list(reversed(gps_obj.trace.strip('.').split('.')))

        next_level = levels.pop()
        remaining_levels = levels

        last_level = self._add_levels(next_level=next_level, current_level=self, remaining_levels=remaining_levels)

        last_level[gps_obj.location] = last_level.get(gps_obj.location, GPSCoordTree(level=gps_obj.location,
                                                                                     kind='leaf'))

        last_level[gps_obj.location][gps_obj.id] = gps_obj

    def _add_levels(self, next_level, current_level, remaining_levels):

        # get current_level.next_level GPSCoordTree if it exists, create empty GPSCoordTree otherwise
        current_level[next_level] = current_level.get(next_level, GPSCoordTree(level=next_level))

        # shift levels one register
        current_level = current_level[next_level]
        try:
            next_level = remaining_levels.pop()

        except IndexError as exc:
            if 'empty list' in exc.message:
                return current_level
            else:
                raise exc

        self._add_levels(next_level=next_level, current_level=current_level, remaining_levels=remaining_levels)


    def get_subtree(self, level):
        """
        Returns a ``GPSCoordTree`` object containing references to all leaves below level:
        :param level: The name of the node that will be the base of the subtree.
        :type level: string
        :returns: a tree containing references to all leaves below level:
        :rtype: GPSCoordTree
        """

        if level in self.keys():
            return self[level]
        else:
            for key in self.keys():
                return self.get_subtree(level=key)





    def mean(self, level):
        """
        Returns a `GPSCoord()` initialized with the mean latitude and longitude of the subtree below level: specified.

        :param level: The name of the deepest node defined in each of your coord objs' `trace` that they have in
        common.

        Example: ``level='Kole'`` will group ``MWA`` and ``OLE``

        coord1's trace -> root.Uganda.Kole.MWA
        coord2's trace -> root.Uganda.Kole.OLE
        coord3's trace -> root.Uganda.Amuru.OKS


        :type level: string
        :return: :mod:`GPSCoord`
        :rtype: :mod:`GPSCoord`
        """




class GPSCoord(Bunch):
    '''
    Class represents a single GPS coordinate.

    VERY SIMPLE RIGHT NOW!
    '''

    def __init__(self, location, lat, lon, trace='', **kwargs):
        """
            Initializes a GPSCoord object.

            :param location:  Text associated with the GPS coord. Does not have to be unique as long as the GPS coords are.
            :type location: `str()`
            :param lat: Latitude value.
            :type lat: `str()`
            :param lon: Longitude Value.
            :type lon: `str()`
            :param trace: A representation of how to group this location in a hierarchical tree structure based on your
            project. If I were working on a set of tsetse fly traps in Uganda, I might use
            'uganda.district_name.county_name.subcounty_name.village_name'.
            :type trace: `str()`
            :return: `self`
            :rtype: `GPSCoord()`
            """
        super(GPSCoord, self).__init__(**kwargs)
        self.location = location
        self.lat = clean_coord(lat)
        self.lon = clean_coord(lon)
        self.trace = trace
        self.id = ':'.join([self.location, str(self.lat), str(self.lon)])

    # def __repr__(self):
    #     return "GPSCoord(location={0}, lat={1}, lon={2}, trace={3})".format(self.location, self.lat, self.lon, self.trace)
    #
    # def __str__(self):
    #     return self.__repr__()


