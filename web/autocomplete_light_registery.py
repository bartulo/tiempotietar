from web.models import Articulo

import autocomplete_light

class ArticuloAutocomplete(autocomplete_light.AutocompleteModelBase):
  search_fields = ['nombre']
autocomplete_light.register(Articulo, ArticuloAutocomplete)
