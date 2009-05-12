# Trivial OGR plugin for Nautilus
#
# Shamelessly adapted from Mercurial Nautilus Plugin
#
# Published under the GNU GPL

import gconf
import gtk
import gobject
import nautilus
import os
import subprocess
import sys
import tempfile
import time
import urllib
from osgeo import ogr

class GisExtension(nautilus.MenuProvider,nautilus.InfoProvider,nautilus.PropertyPageProvider):

    def __init__(self):
        pass
    
    def _about_cb(self, window, vfs_file):
        pass

    def get_file_items(self, window, vfs_files):
        mainitem = nautilus.MenuItem('OgrNautilus', 'OgrInfo', 'Do something')
        return mainitem,

    def update_file_info(self, file):
        '''Return emblem and hg status for this file'''
        file.add_string_attribute('ogr_status', '?')
    
    def __add_row(self, table, row, label_item, label_value):
        label = gtk.Label(label_item)
        label.set_use_markup(True)
        label.set_alignment(1, 0)
        table.attach(label, 0, 1, row, row + 1, gtk.FILL, gtk.FILL, 0, 0)
        label.show()

        label = gtk.Label(label_value)
        label.set_use_markup(True)
        label.set_alignment(0, 1)
        label.show()
        table.attach(label, 1, 2, row, row + 1, gtk.FILL, 0, 0, 0)
   
    def get_path_for_vfs_file(self, vfs_file):
        if vfs_file.get_uri_scheme() != 'file':
            return None
        return urllib.unquote(vfs_file.get_uri()[7:])
    
    def __get_feature_info(self, vfs_files):
	if len(vfs_files) != 1:
            return
        file = vfs_files[0]
        path = self.get_path_for_vfs_file(file)
        if path is None or file.is_directory():
            return
        shapeFile = ogr.Open(path)
	layer = shapeFile.GetLayer(0)
	featureCount = layer.GetFeatureCount()
	geometryColumnValue = layer.GetLayerDefn().GetGeomType()
	if   geometryColumnValue == 0: geometryColumn = "Unknown"
  	elif geometryColumnValue == 1: geometryColumn = "Point"
	elif geometryColumnValue == 2: geometryColumn = "LineString"
	elif geometryColumnValue == 3: geometryColumn = "Polygon"
	elif geometryColumnValue == 4: geometryColumn = "MultiPoint"
	elif geometryColumnValue == 5: geometryColumn = "MultiLineString"
	elif geometryColumnValue == 6: geometryColumn = "MultiPolygon"
	elif geometryColumnValue == 7: geometryColumn = "GeometryCollection"

	return geometryColumn, featureCount,

    def get_property_pages(self, vfs_files):
        self.property_label = gtk.Label('OgrInfo')
	
	featureInfo = self.__get_feature_info(vfs_files)

        table = gtk.Table(7, 2, False)
        table.set_border_width(5)
        table.set_row_spacings(5)
        table.set_col_spacings(5)

        self.__add_row(table, 0, '<b>Features</b>:', featureInfo[1])
        self.__add_row(table, 1, '<b>Geometry</b>:', featureInfo[0])
        
        table.show()

        return nautilus.PropertyPage("OGRPropertyPage::status",
                                     self.property_label, table),


