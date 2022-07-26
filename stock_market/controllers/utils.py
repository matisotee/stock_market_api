from rest_framework.authentication import TokenAuthentication as DjangoTokenAuthentication


class TokenAuthentication(DjangoTokenAuthentication):
    keyword = 'Bearer'
