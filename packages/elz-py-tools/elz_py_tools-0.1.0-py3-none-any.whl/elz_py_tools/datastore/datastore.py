from ..drivers import GraphDriver, MongoDriver
from .types_register import TypesRegister


class Datastore(object):
    """ Datastore for uniformizing query to graph and mongo databases """

    _types_register: TypesRegister
    _graph_driver: GraphDriver
    _mongo_driver: MongoDriver

    def __init__(self, types_register: TypesRegister, graph_driver: GraphDriver = None, mongo_driver: MongoDriver = None):
        self._types_register = types_register
        self._graph_driver = graph_driver
        self._mongo_driver = mongo_driver

    def get_mongo_driver(self):
        return self._mongo_driver

    def get_graph_driver(self):
        return self._graph_driver

    def close_connections(self):
        """ Close driver connections """
        self._mongo_driver.close()

    async def get_objects(self, typename: str):
        """ Return all objects of type defined in argument
            Results are merged objects of triplestore and mongo databases
        """
        if not self._types_register.exists_type(typename):
            raise Exception(f'Unknow type {typename}')

        graph_type, mongo_collection = self._types_register.resolve_type(typename)

        graph_objects = []
        mongo_objects = []
        if self._graph_driver and graph_type:
            graph_objects = await self._graph_driver.get_nodes(graph_type)
        if self._mongo_driver and mongo_collection:
            mongo_objects = self._mongo_driver.find_documents(mongo_collection)

        merged_objects = []
        mongo_objects_id = list(map(lambda x: x['id'], mongo_objects))
        if graph_type:
            for graph_object in graph_objects:
                matching_mongo_object = next((obj for obj in mongo_objects if obj['id'] == graph_object['id']), None) or {}
                merged_objects.append({
                    **graph_object,
                    **matching_mongo_object,
                    "type": typename
                })
        else:
            merged_objects = mongo_objects
        return merged_objects

    async def get_object(self, typename: str, object_id: str):
        """ Return object corresponding to id and type defined in argument
            Result is merge of object found in triplestore and mongo databases if any
        """
        if not self._types_register.exists_type(typename):
            raise Exception(f'Unknow type {typename}')

        graph_type, mongo_collection = self._types_register.resolve_type(typename)
        graph_object = {}
        mongo_object = {}

        if self._graph_driver and graph_type:
            graph_object = await self._graph_driver.get_node(graph_type, object_id)
            graph_object = graph_object or {}
        if self._mongo_driver and mongo_collection:
            mongo_object = self._mongo_driver.find_document(mongo_collection, object_id) or {}

        merged_object = {
            **graph_object,
            **mongo_object,
            "type": typename
        }
        return merged_object
