import os
import unittest
from typing import Any, Dict, Union

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_project.settings")
import django
django.setup()


from graphene.test import Client
from django_app_graphql import schema


class AbstractGraphQLTest(unittest.TestCase):
    """
    An abstract class that can be used to perform tests on a graphql server.
    To perform tests, just do the following:

    .. code-block:: python

        from django_app_graphql import tests
        class MyGraphQLTests(tests.AbstractGraphQLTest):

            def test_foobar_query():
                # your test

    Generally speaking there are 2 ways of performing query: linear or chaining.

    Linear testing is when you in one command perform a grpahql query and then check the satisfaction of an assertion:

    .. code-block :: python

        self.assert_query_data_equal("foobar(5) { id }") # perform a grpahql query and check the result

    Chaining testing is when you first perform the query and then check the satisfaction of an assertion:

    .. code-block :: python

        result = self.check_query("foobar(5) { id }") # perform query
        self.assert_query_data_equal(result) # check the result

    Linear is quick, but chaining tsting allows you to check multiple assertions in one batch

    """

    graphql_client: Client = None

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.graphql_client = Client(schema=schema.schema)

    def check_query(self, query: Union[str, Dict[str, any]], context) -> Dict[str, any]:
        if isinstance(query, Dict):
            return query
        elif isinstance(query, str):
            pass
        else:
            raise TypeError(f"query should either be a dictionary or a string!")

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

    def check_mutation(self, mutation: Union[str, Dict[str, any]], context) -> Dict[str, any]:
        if isinstance(mutation, Dict):
            return mutation
        elif isinstance(mutation, str):
            pass
        else:
            raise TypeError(f"query should either be a dictionary or a string!")

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

    def _check(self, query_type: str, q: Union[str, Dict[str, any]], context)  -> Dict[str, any]:
        if query_type == "query":
            return self.check_query(q, context)
        elif query_type == "mutation":
            return self.check_mutation(q, context)
        else:
            raise ValueError(f"invalid type! Only mutation or query are allowed!")

    def _assert_data_equal(self, query_type: Union[str, Dict[str, any]], query: str, expected, context=None):
        output = self._check(query_type, query, context)
        assert output == expected

    def _assert_data_contains_key(self, query_type: Union[str, Dict[str, any]], query: str, key: str, context=None):
        output = self._check(query_type, query, context)
        assert key in output

    def _assert_data_key_value(self, query_type: str, query: Union[str, Dict[str, any]], key: str, value: Any, context=None):
        output = self._check(query_type, query, context)

        assert key in output
        assert output[key] is not None
        assert output[key] == value

    def assert_query_data_equal(self, query: Union[str, Dict[str, any]], expected, context=None):
        """
        Check if the whole returned value of a graphql query/mutation is exactly as the one provided by the user

        :param query: either a strijng, repersenting the query that we need to perform or a a dictionary,
            representing the (assumed) output of check_query/check_mutation.
        :param expected: expected data value
        :param context: variables
        :return:
        """
        return self._assert_data_equal("query", query, expected, context)

    def assert_mutation_data_equal(self, mutation: Union[str, Dict[str, any]], expected, context=None):
        """
        Check if the whole returned value of a graphql query/mutation is exactly as the one provided by the user

        :param mutation: either a strijng, repersenting the mutation that we need to perform or a a dictionary,
            representing the (assumed) output of check_query/check_mutation.
        :param expected: expected data value
        :param context: variables
        :return:
        """
        return self._assert_data_equal("mutation", mutation, expected, context)

    def assert_query_data_contains_key(self, query: Union[str, Dict[str, any]], key: str, context=None):
        return self._assert_data_contains_key("query", query, key, context)

    def assert_mutation_data_contains_key(self, mutation: Union[str, Dict[str, any]], key: str, context=None):
        return self._assert_data_contains_key("mutation", mutation, key, context)

    def assert_query_data_key_value(self, query: Union[str, Dict[str, any]], key: str, value: Any, context=None):
        return self._assert_data_key_value("query", query, key, value, context)

    def assert_mutation_data_key_value(self, mutation: Union[str, Dict[str, any]], key: str, value: Any, context=None):
        return self._assert_data_key_value("mutation", mutation, key, value, context)




# Create your tests here.