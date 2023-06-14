from SupplierApp.backends import EmailBackend
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, SupplierSerializer,  RankingSerializer
from .models import Supplier,  Ranking
import numpy as np
from utils.calculate_ahp import ahp
# Registration


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Perform password hashing
            hashed_password = make_password(
                serializer.validated_data['password'])

            # Remove the 'password' key from the validated data
            del serializer.validated_data['password']

            # Create the user instance with the validated serializer data
            user = User.objects.create(
                password=hashed_password, **serializer.validated_data)

            # Perform any additional actions (e.g., sending confirmation email)
            # ...

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login


class LoginView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = EmailBackend().authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
# AHP calculate


def AHPCalculate():
    suppliers = Supplier.objects.all()

    if not suppliers:
        return []

    supplier_names = [supplier.name for supplier in suppliers]
    supplier_matrix = np.array([
        [supplier.financial_status for supplier in suppliers],
        [supplier.quality for supplier in suppliers],
        [supplier.service for supplier in suppliers],
        [supplier.reputation for supplier in suppliers],
        [supplier.technical_capability for supplier in suppliers],
        [supplier.price_cost for supplier in suppliers]
    ])

    print("Matrix", supplier_matrix)

    # Normalize the supplier matrix
    normalized_supplier_matrix = supplier_matrix / \
        supplier_matrix.sum(axis=1, keepdims=True)

    print("Normalized Supplier Matrix", normalized_supplier_matrix)

    # Get AHP values from the ahp function
    priority_weights, _, _ = ahp()

    # Multiply each row of the normalized supplier matrix with the corresponding row of the priority weights
    alternative_results = normalized_supplier_matrix.T * priority_weights

    # Sum the results of element-wise multiplications to calculate the final result
    results = np.sum(alternative_results, axis=1)

    # Rank the suppliers
    ranked_indices = np.argsort(-results)
    ranked_suppliers = []
    for i, idx in enumerate(ranked_indices):
        supplier_name = supplier_names[idx]
        supplier_result = results[idx]
        supplier_ranking = i + 1
        ranked_suppliers.append({
            'name': supplier_name,
            'result': supplier_result,
            'ranking': supplier_ranking
        })

    return ranked_suppliers


check = AHPCalculate()
for i in check:
    print(i)

# AHP calculation endpoints


class RankingListView(APIView):
    def get(self, request):
        rankings = AHPCalculate()

        return Response(rankings)


class RankingCreateView(generics.ListCreateAPIView):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer

    def post(self, request, *args, **kwargs):
        serializer = RankingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Get the validated data from the serializer
            validated_data = serializer.validated_data

            # Access the data from the validated serializer data
            supplier_name = validated_data['supplier']['name']
            results = validated_data['results']
            ranking = validated_data['ranking']

            # Perform your ranking computation logic here
            # ...

            # Create a new instance of Ranking model with the computed ranking
            ranking_instance = Ranking.objects.create(
                supplier_name=supplier_name,
                results=results,  # Update with your computed results
                ranking=ranking,
                # Add any other fields required by your Ranking model
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
