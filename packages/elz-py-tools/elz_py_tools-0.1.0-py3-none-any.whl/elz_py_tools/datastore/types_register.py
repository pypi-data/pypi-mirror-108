import os
import json


class TypesRegister(object):
    """ A register for types defined in database
        Types in constructor input must be a list of dicts with keys : { name, node, mongo }
        - name: a name identifier for this type
        - node: node type with prefix used for this type in triplestore
        - mongo: name of mongo collection used for this type
    """

    def __init__(self, types):
        self._types = types
        self.check_types()

    def check_types(self):
        """ Check integrity for types defined """
        prefixes = json.loads(os.environ["NAMESPACE_MAPPING"]).keys()
        for type_def in self._types:
            if "node" not in type_def and "mongo" not in type_def:
                raise Exception(f'Type {type_def["name"]} must be defined at least for "node" or "mongo key"')
            if "node" in type_def:
                if ':' not in type_def["node"]:
                    raise Exception(f'Type {type_def["name"]} has no prefix defined for node type')
                elif type_def["node"].split(':')[0] not in prefixes:
                    raise Exception(f'Type {type_def["name"]} has a node type with a prefix not defined in namespace mapping')

    def exists_type(self, typename: str):
        """ Return if obj_type in argument exists in types registered """
        return self._find_matching_type(typename) is not None

    def resolve_type(self, typename: str):
        """ Returns a tuple (node_type, mongo_collection) for type name in argument """
        type_def = self._find_matching_type(typename)
        graph_type = type_def.get('node', None)
        mongo_collection = type_def.get('mongo', None)
        if mongo_collection:
            mongo_collection = f'{mongo_collection.lower()}s'
        return graph_type, mongo_collection

    def _find_matching_type(self, typename: str):
        """ Find matching type definition for type name in argument """
        for type_def in self._types:
            if type_def['name'] == typename:
                return type_def
        return None
