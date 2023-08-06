import json
import os
import datetime
from .publisher import GraphPublisher
from .parser import parse_construct_result
from .sparql import SPARQLBuilder


class GraphDriver(object):
    """ Driver for triplestore database """

    def __init__(self, amqp_client, sender_id, repository_name, prefixes_mapping, nodes_namespace_uri, nodes_prefix):
        self._publisher = GraphPublisher(amqp_client, sender_id, repository_name)
        self._sparql_builder = SPARQLBuilder(prefixes_mapping, nodes_namespace_uri, nodes_prefix)
        self._prefixes_mapping = prefixes_mapping
        self._nodes_namespace_uri = nodes_namespace_uri
        self._nodes_prefix = nodes_prefix

    def get_graph_publisher(self):
        return self._publisher

    async def raw_select(self, query: str):
        """ Executes a raw select query
            Is equivalent to get publisher from this object and call its select method
        """
        result = await self._publisher.select(query)
        return result

    async def raw_construct(self, query: str, parse_result=True):
        """ Executes a raw construct query
            if parse_result is True, parse bindings result and convert into properties grouped by entity returned
        """
        bindings = await self._publisher.construct(query)
        if parse_result:
            objects = parse_construct_result(bindings)
        else:
            objects = bindings
        return objects

    async def get_nodes(self, node_type: str):
        """ Get nodes and their properties corresponding to node_type """
        sparql_query = self._sparql_builder.build_construct_objects_query(node_type)
        bindings = await self._publisher.construct(sparql_query)
        objects = parse_construct_result(bindings)
        for obj in objects:
            obj['id'] = self.to_prefixed_uri(obj['id'])
        return objects

    async def get_node(self, node_type: str, object_id: str):
        """ Get node and its properties for node_type and object_id """
        sparql_query = self._sparql_builder.build_construct_object_query(node_type, self.to_absolute_uri(object_id))
        bindings = await self._publisher.construct(sparql_query)
        objects = parse_construct_result(bindings)
        for obj in objects:
            obj['id'] = self.to_prefixed_uri(obj['id'])
        return objects[0]

    def to_absolute_uri(self, uri: str):
        """ Convert an uri into absolute uri """
        if uri.startswith('http://'):
            return uri
        elif self._nodes_prefix in uri:
            return uri.replace(f'{self._nodes_prefix}:', f':{self._nodes_namespace_uri}/')
        else:
            matching_prefix = next((prefix for prefix in self._prefixes_mapping.keys() if prefix in uri), None)
            if matching_prefix:
                return uri.replace(f'{matching_prefix}:', self._prefixes_mapping[matching_prefix])
        # Last case: no prefix at all, we put nodes namespace uri
        return f'{self._nodes_namespace_uri}/{uri}'

    def to_prefixed_uri(self, uri: str):
        """ Convert an uri into prefixed uri """
        if ':' not in uri and '#' not in uri:
            raise Exception(f'Uri {uri} cannot be prefixed with alias as there is no uri prefix')
        if self._nodes_namespace_uri in uri:
            return uri.replace(f'{self._nodes_namespace_uri}/', f'{self._nodes_prefix}:')
        else:
            prefix, ns_uri = next(
                ((prefix, ns_uri) for prefix, ns_uri in self._prefixes_mapping.items() if ns_uri in uri), None
            )
            if ns_uri:
                if '#' in uri:
                    return uri.replace(f'{ns_uri}#', f'{prefix}:')
                else:
                    return uri.replace(f'{ns_uri}/', f'{prefix}:')

        # Last case: no prefix at all, we put nodes prefix
        return f'{self._nodes_prefix}:{uri}'
