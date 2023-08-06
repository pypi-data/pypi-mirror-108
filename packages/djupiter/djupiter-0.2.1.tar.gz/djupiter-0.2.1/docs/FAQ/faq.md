# Frequently Asked Questions

## How do I register my custom views to the Swagger UI docs?

You need to add the `swagger_auto_schema` decorator to your view.

```py
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from djupiter.serializers import GenericDetailSerializer


@swagger_auto_schema(
    method="GET",
    responses={
        200: GenericDetailSerializer,
    },
)
def example(request):
    """
    Example endpoint. Don't forget to delete me!
    """
    return Response({"message": "hello, world!"}, status=200)
```

## How do I use my token for authentication?

Use the `Authentication: Token <token>` header in your requests.

```console
# Using curl
$ curl -i -H "Accept: application/json" -H "Authentication: Token example-token-123" http://127.0.0.1/api/me/
# Using HTTPie
$ http http://127.0.0.1/api/me/ "Authentication: Token example-token-123"
```

```js
// Fetch API
fetch("http://127.0.0.1/api/me/", {
    headers: {
        "Authentication": "Token example-token-123"
    },
});

// Axios
axios.get("http://127.0.0.1/api/me/", {
    headers: {
        "Authentication": "Token example-token-123"
    },
});
```
