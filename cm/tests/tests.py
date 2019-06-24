import unittest
from werkzeug.exceptions import NotFound
from app import create_app
import os.path
from shutil import copyfile
from .test_client import TestClient
UPLOAD_DIRECTORY = '/var/hotmaps/cm_files_uploaded'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    os.chmod(UPLOAD_DIRECTORY, 0o777)


class TestAPI(unittest.TestCase):


    def setUp(self):
        self.app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = TestClient(self.app,)

    def tearDown(self):

        self.ctx.pop()


    def test_compute(self):
        raster_file_dir = 'tests/data'
        
        raster_file_path1 = raster_file_dir + "/NUTS3_cut_id_number.tif"
        raster_file_path2 = raster_file_dir + "/RESULTS_GFA_RES_BUILD.tif"
        raster_file_path3 = raster_file_dir + "/RESULTS_ENERGY_HEATING_RES_2012.tif"
        raster_file_path4 = raster_file_dir + "/LAU2_id_number.tif"
        raster_file_path5 = raster_file_dir + "/GHS_BUILT_1975_100_share.tif"
        raster_file_path6 = raster_file_dir + "/GHS_BUILT_1990_100_share.tif"
        raster_file_path7 = raster_file_dir + "/GHS_BUILT_2000_100_share.tif"
        raster_file_path8 = raster_file_dir + "/GHS_BUILT_2014_100_share.tif"

        # simulate copy from HTAPI to CM
        save_path1 = UPLOAD_DIRECTORY+"/NUTS3_cut_id_number.tif"
        save_path2 = UPLOAD_DIRECTORY+"/RESULTS_GFA_RES_BUILD.tif"
        save_path3 = UPLOAD_DIRECTORY+"/RESULTS_ENERGY_HEATING_RES_2012.tif"
        save_path4 = UPLOAD_DIRECTORY+"/LAU2_id_number.tif"
        save_path5 = UPLOAD_DIRECTORY+"/GHS_BUILT_1975_100_share.tif"
        save_path6 = UPLOAD_DIRECTORY+"/GHS_BUILT_1990_100_share.tif"
        save_path7 = UPLOAD_DIRECTORY+"/GHS_BUILT_2000_100_share.tif"
        save_path8 = UPLOAD_DIRECTORY+"/GHS_BUILT_2014_100_share.tif"
        
        copyfile(raster_file_path1, save_path1)
        copyfile(raster_file_path2, save_path2)
        copyfile(raster_file_path3, save_path3)
        copyfile(raster_file_path4, save_path4)
        copyfile(raster_file_path5, save_path5)
        copyfile(raster_file_path6, save_path6)
        copyfile(raster_file_path7, save_path7)
        copyfile(raster_file_path8, save_path8)


        inputs_raster_selection = {}
        inputs_parameter_selection = {}
        inputs_vector_selection = {}
        inputs_raster_selection["nuts_id"] = save_path1
        inputs_raster_selection["gfa_res"] = save_path2
        inputs_raster_selection["energy_res"] = save_path3
        inputs_raster_selection["lau2_id"] = save_path4
        inputs_raster_selection["cp_share_1975"] = save_path5
        inputs_raster_selection["cp_share_1990"] = save_path6
        inputs_raster_selection["cp_share_2000"] = save_path7
        inputs_raster_selection["cp_share_2014"] = save_path8
        

        # register the calculation module a
        payload = {"inputs_raster_selection": inputs_raster_selection,
                   #"inputs_parameter_selection": inputs_parameter_selection,
                   #"inputs_vector_selection": inputs_vector_selection
                   }


        rv, json = self.client.post('computation-module/compute/', data=payload)

        self.assertTrue(rv.status_code == 200)


