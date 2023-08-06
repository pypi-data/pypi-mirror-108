from django.conf import settings
from appconf import AppConf


class DjangoAppGraphQLAppConf(AppConf):
    class Meta:
        prefix = "DJANGO_APP_GRAPHQL"

    EXPOSE_GRAPHIQL = True
    """
    If set, we will expose the graphiql UI
    """
    GRAPHQL_SERVER_URL = ""
    """
    the endpoint where the graphql server is located
    """

