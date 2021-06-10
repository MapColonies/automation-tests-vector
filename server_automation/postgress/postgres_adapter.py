from server_automation.configuration import config
from mc_automation_tools import common, postgres


def create_full_table(table_name=config.PG_TABLE_NAME):
    client = postgres.PGClass(config.PG_HOST, config.PG_DB_NAME, config.PG_USER, config.PG_PASS)
    commands = [f"CREATE TABLE {table_name} "
                "(entity_id UUID PRIMARY KEY,"
                "layer_id VARCHAR(255) NOT NULL,"
                "name VARCHAR(255),"
                "type VARCHAR(255),"
                "increment_index serial,"
                "diff integer NOT NULL,"
                "dateCreation TIMESTAMP NOT NULL,"
                "updateCreation TIMESTAMP NOT NULL,"
                "polygon geometry,"
                "json_object JSON NOT NULL)",
                "CREATE INDEX geo_coordinate_idx ON v_buildings USING GIST(polygon)"]

    client.command_execute(commands)
    pass


def insert_entity_to_db(entities_params, table_name=config.PG_TABLE_NAME):
    """
    This method insert list of params into table :param table_name:table to insert - as default take name from
    config=> PG_TABLE_NAME :param entities_params: dictionary including keys: uuid[str], layer_id[str], name[str],
    layer_type[str], cdatetime[str], udatetime[str], geo_json[json], entity_json[str]
    """
    client = postgres.PGClass(config.PG_HOST, config.PG_DB_NAME, config.PG_USER, config.PG_PASS)
    body = f'INSERT INTO "{table_name}"("entity_id","layer_id","name","type","diff",dateCreation,updateCreation,"polygon","json_object")' \
           f"VALUES"
    values = ""
    for params in entities_params:
        uuid = params['uuid']
        layer_id = params['layer_id']
        name = params['name']
        ltype = params['layer_type']
        diff = params['diff']
        cdatetime = params['cdatetime']
        udatatime = params['udatatime']
        geo_json = params['geo_json']
        entity_json = params['entity_json']
        value = f"('{uuid}','{layer_id}','{name}','{ltype}','{diff}','{cdatetime}','{udatatime}',ST_GeomFromGeoJSON('{geo_json}'),'{entity_json}')"
        values = values + "," + value
    command = body+values[1:]
    client.command_execute([command])


def get_last_insertion_idx(column='increment_index', table_name=config.PG_TABLE_NAME):
    client = postgres.PGClass(config.PG_HOST, config.PG_DB_NAME, config.PG_USER, config.PG_PASS)
    res = client.get_column_by_name(table_name=table_name, column_name=column)
    return max(res)


def get_all_entities_id(table_name=config.PG_TABLE_NAME):
    client = postgres.PGClass(config.PG_HOST, config.PG_DB_NAME, config.PG_USER, config.PG_PASS)
    return client.get_column_by_name(table_name, 'entities_id')
