# based on data : https://github.com/Microsoft/USBuildingFootprints

from datetime import datetime

import geojson

from server_automation.support_utilities import layer_generator
from server_automation.configuration import config
import os
# Z_TIME = datetime.now().strftime('vector_%Y%m_%d_%H_%M_%S')
# output_dir = layer_generator.generate_single_full_json(config.LAYER_ID_B, Z_TIME)
#
# output_dir = os.path.join(config.STORE_DATA_DIR, 'vector_data', Z_TIME)
# layer_generator.generate_entity_file(config.LAYER_ID_B, 1, 'entities', 10, output_dir)

# geojson.utils.generate_random("Polygon")
layer_generator.generate_entity_json(source='/home/ronenk1/dev/automation-tests-vector/geojsons/small_70k_Alaska.geojson')