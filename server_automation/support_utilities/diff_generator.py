"""This module responsible to generate diff files"""
import enum
from server_automation.configuration import config
from server_automation.postgress import postgres_adapter
# from mc_automation_tools import


class RandomDiffOpt(enum.Enum):
    add_tag = 1
    no_change = 2
    delete = 3
    insert = 4
    geometry = 5


def generate_new_diff(layer_id, n_zips=10, n_files=10, n_objects=10, samples=config.DIFF_SAMPLES,
                      output_dir=config.STORE_DATA_DIR, source=config.DEBUG_ENTITY_FILE):
    full_entities_id = postgres_adapter.get_all_entities_id()
    pass
