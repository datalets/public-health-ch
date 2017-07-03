from wagtail.api.v2.router import WagtailAPIRouter
from .endpoints import EntriesAPIEndpoint

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('entries', EntriesAPIEndpoint)
