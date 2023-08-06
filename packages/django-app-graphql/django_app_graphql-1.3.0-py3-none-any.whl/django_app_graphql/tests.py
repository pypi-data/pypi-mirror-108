import os
import unittest
from typing import Any

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_project.settings")
import django
django.setup()


from graphene.test import Client
from django_app_graphql import schema


class AbstractGraphQLTest(unittest.TestCase):

    graphql_client: Client = None

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.graphql_client = Client(schema=schema.schema)

    def check_query(self, query, context):
        query = f"""
        query {{
            {query}
        }}
        """
        executed = self.graphql_client.execute(query, context=context)
        assert 'data' in executed, "GraphQL output should return 'data', but this call did not."
        assert 'errors' not in executed, f"Got graphQL errors: {executed}"
        assert executed['data'] is not None, f"data paylaod is None. Output={executed}"
        return executed['data']

    def check_mutation(self, mutation, context):
        mutation = f"""
        mutation {{
            {mutation}
        }}
        """
        executed = self.graphql_client.execute(mutation, context=context)
        assert 'data' in executed, "GraphQL output should return 'data', but this call did not."
        assert 'errors' not in executed, f"Got graphQL errors: {executed}"
        assert executed['data'] is not None, f"data paylaod is None. Output={executed}"
        return executed['data']

    def _check(self, query_type: str, q: str, context):
        if query_type == "query":
            return self.check_query(q, context)
        elif query_type == "mutation":
            return self.check_mutation(q, context)
        else:
            raise ValueError(f"invalid type! Only mutation or query are allowed!")

    def _assert_data_equal(self, query_type: str, query: str, expected, context=None):
        output = self._check(query_type, query, context)
        assert output == expected

    def _assert_data_contains_key(self, query_type: str, query: str, key: str, context=None):
        output = self._check(query_type, query, context)
        assert key in output

    def _assert_data_key_value(self, query_type: str, query: str, key: str, value: Any, context=None):
        output = self._check(query_type, query, context)

        assert key in output
        assert output[key] is not None
        assert output[key] == value

    def assert_query_data_equal(self, query, expected, context=None):
        return self._assert_data_equal("query", query, expected, context)

    def assert_mutation_data_equal(self, query, expected, context=None):
        return self._assert_data_equal("mutation", query, expected, context)

    def assert_query_data_contains_key(self, query: str, key: str, context=None):
        return self._assert_data_contains_key("query", query, key, context)

    def assert_mutation_data_contains_key(self, query: str, key: str, context=None):
        return self._assert_data_contains_key("mutation", query, key, context)

    def assert_query_data_key_value(self, query:str, key: str, value: Any, context=None):
        return self._assert_data_key_value("query", query, key, value, context)

    def assert_mutation_data_key_value(self, query: str, key: str, value: Any, context=None):
        return self._assert_data_key_value("mutation", query, key, value, context)




# Create your tests here.