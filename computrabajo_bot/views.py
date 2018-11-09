from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from computrabajo_bot.serializers import ComputrabajoSerializer
from computrabajo_bot.tasks import process_request


class ComputrabajoAPIVIew(APIView):
    def post(self, request):
        """
        validate data and process request in an async task
        """
        # get request params
        ser = ComputrabajoSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=HTTP_400_BAD_REQUEST)

        process_request.delay(request.data)
        return Response({'status': 'ok'}, status=HTTP_200_OK)