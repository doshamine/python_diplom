from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from .tasks import send_mail_task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .filters import ProductFilter
from .models import Product, Order, Contact, OrderStatus, ContactType
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, ContactSerializer
from .tasks import do_import


@staff_member_required
def import_view(request):
    do_import.delay()
    return redirect('/admin/')

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)

                send_mail_task.delay(
                    subject='Успешная регистрация',
                    message='Спасибо за регистрацию на нашем сайте!',
                    recipient_list=[user.email],
                )

                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all().prefetch_related('product_info__shop')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'model']
    ordering_fields = ['name', 'model', 'product_info__price']


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).exclude(status=OrderStatus.NEW)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(OrderViewSet):
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status=OrderStatus.NEW)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        contact = serializer.save(user=self.request.user)
        if contact.type == ContactType.ADDRESS:
            send_mail_task.delay(
                subject='Подтверждение адреса',
                message=f'Ваш адрес "{contact.value}" был успешно добавлен.',
                recipient_list=[contact.user.email],
            )


class OrderConfirmAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        contact_id = request.data.get('contact_id')

        if not order_id or not contact_id:
            return Response({'error': 'order_id and contact_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if order.status != OrderStatus.NEW:
            return Response({'error': 'Only new orders can be confirmed.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)

        order.status = OrderStatus.PAID
        order.save()

        return Response({'message': 'Order confirmed successfully.'}, status=status.HTTP_200_OK)