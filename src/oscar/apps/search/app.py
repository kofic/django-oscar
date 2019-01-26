from django.conf.urls import url

from oscar.apps.search import facets
from oscar.core.application import Application
from oscar.core.loading import get_class

is_solr_supported = get_class('search.features', 'is_solr_supported')


class SearchApplication(Application):
    name = 'search'
    search_view = get_class('search.views', 'FacetedSearchView')
    search_form = get_class('search.forms', 'SearchForm')

    def get_urls(self):

        urlpatterns = []

        if is_solr_supported():
            from haystack.views import search_view_factory

            # The form class has to be passed to the __init__ method as that is how
            # Haystack works.  It's slightly different to normal CBVs.
            urlpatterns = [
                url(r'^$', search_view_factory(
                    view_class=self.search_view,
                    form_class=self.search_form,
                    searchqueryset=self.get_sqs()),
                    name='search'),
            ]

        return self.post_process_urls(urlpatterns)

    def get_sqs(self):
        """
        Return the SQS required by a the Haystack search view
        """
        return facets.base_sqs()


application = SearchApplication()
