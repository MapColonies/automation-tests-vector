# based on data : https://github.com/Microsoft/USBuildingFootprints
# https://www.microsoft.com/en-us/maps/building-footprints
from datetime import datetime

import geojson

from server_automation.support_utilities import layer_generator, diff_generator
from server_automation.configuration import config
import os
# Z_TIME = datetime.now().strftime('vector_%Y%m_%d_%H_%M_%S')
# output_dir = layer_generator.generate_single_full_json(config.LAYER_ID_B, Z_TIME)
#
# output_dir = os.path.join(config.STORE_DATA_DIR, 'vector_data', Z_TIME)
# layer_generator.generate_entity_file(config.LAYER_ID_B, 1, 'entities', 10, output_dir)

# geojson.utils.generate_random("Polygon")
# layer_generator.generate_entity_json(source=config.DEBUG_ENTITY_FILE)






layer_generator.generate_single_full_json(layer_id=config.LAYER_ID_B,
                                          n_zips=10,
                                          n_files=10,
                                          n_objects=700,
                                          output_dir=config.STORE_DATA_DIR)

# from server_automation.postgress import postgres_adapter

res = diff_generator.generate_new_diff(layer_id=config.LAYER_ID_B)
output_file = res['storage']
res = diff_generator.create_diff_json(res['storage'], config.LAYER_ID_B, res['zips'])
print(res)
body = config.DIFF_SKELETON
body['files'].clear()
body['files'] = [res]
import json
with open(os.path.join(output_file,'diff.json'),'w') as fp:
    json.dump(body,fp)