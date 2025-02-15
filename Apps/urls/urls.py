from .account_urls import urlpatterns as account_urls
from .jwt_urls import urlpatterns as jwt_urls
from .note_urls import urlpatterns as note_urls
urlpatterns = []
urlpatterns.extend(account_urls)
urlpatterns.extend(jwt_urls)
urlpatterns.extend(note_urls)