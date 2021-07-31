from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def test_api(request):
    print(request.POST)
    return Response({"test": "test"}, 200)