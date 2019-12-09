from collections import OrderedDict

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from apps.datos.permissions import IsCustomUser
from apps.datos.reports import generate_xls_report
from apps.utils.shortcuts import get_object_or_none
from apps.utils.viewsets import CustomPagination
from .models import CustomUser, Transaction
from .serializers import CustomUserSerializer, TransaccionSerializer
from .constants import ACTIVE

# Create your views here.


class Osw4lViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination


class CustomUserViewSet(Osw4lViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated, IsCustomUser], methods=['GET'])
    def transactions(self, request):
        queryset = Transaction.objects.filter(
            user=request.user,
            status=ACTIVE
        ).order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TransaccionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransaccionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[IsAuthenticated, IsCustomUser], methods=['GET'])
    def points(self, request):
        return Response({
            'points': request.user.get_points()
        })

    @action(detail=False, permission_classes=[IsAuthenticated, IsCustomUser], methods=['GET'])
    def export_to_excel(self, request):
        return generate_xls_report(request.user)


class TransactionViewSet(Osw4lViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransaccionSerializer
    permission_classes = [IsAuthenticated, IsCustomUser]

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return qs

    @action(detail=True, permission_classes=[IsAuthenticated, IsCustomUser], methods=['PUT'])
    def disable(self, request, pk=None):
        transaction = get_object_or_none(Transaction, id=pk)
        response = {'message': 'this transaction doesnt exist'}
        status = HTTP_400_BAD_REQUEST
        if transaction:
            transaction.disable_transaction()
            response['message'] = 'success'
            status = HTTP_200_OK
        return Response(response, status=status)


