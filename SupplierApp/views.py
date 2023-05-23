from rest_framework.response import Response
import numpy as np
from rest_framework import generics,  status
from .models import Supplier, AHPcalculation, Criteria, Weights, BenefitCost
from .serializers import SupplierSerializer, AHPcalculationSerializer, CriteriaSerializer, WeightsSerializer, BenefitCostSerializer
# Supplier


class SupplierListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating Supplier instances.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific Supplier instance.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a new Supplier instance.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating an existing Supplier instance.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Supplier instance.
        """
        instance.delete()


# Criteria
class CriteriaListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating Criteria instances.
    """
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer


class CriteriaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific Criteria instance.
    """
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a new Criteria instance.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating an existing Criteria instance.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Criteria instance.
        """
        instance.delete()


# Weights
class WeightsListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating Weights instances.
    """
    queryset = Weights.objects.all()
    serializer_class = WeightsSerializer


class WeightsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific Weights instance.
    """
    queryset = Weights.objects.all()
    serializer_class = WeightsSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a new Weights instance.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating an existing Weights instance.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Weights instance.
        """
        instance.delete()


# Benefit and Cost
class BenefitCostListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating BenefitCost instances.
    """
    queryset = BenefitCost.objects.all()
    serializer_class = BenefitCostSerializer


class BenefitCostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific BenefitCost instance.
    """
    queryset = BenefitCost.objects.all()
    serializer_class = BenefitCostSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a new BenefitCost instance.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating an existing BenefitCost instance.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a BenefitCost instance.
        """
        instance.delete()

# AHP calculation


class AHPcalculationListCreateView(generics.ListCreateAPIView):
    queryset = AHPcalculation.objects.all()
    serializer_class = AHPcalculationSerializer

    def create(self, request, *args, **kwargs):
        criteria_values = request.data.get('criteria_values', [])
        supplier_id = request.data.get('supplier', None)

        # 1. Define the Decision Hierarchy
        criteria_queryset = Criteria.objects.all()
        criteria_count = criteria_queryset.count()
        if criteria_count < 2:
            return Response({'detail': 'At least 2 criteria are required for AHP calculation.'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Perform Pairwise Comparisons
        pairwise_matrix = [
            [1.0] * criteria_count for _ in range(criteria_count)]
        # Update pairwise_matrix based on pairwise comparisons of criteria

        # 3. Calculate the Weighted Sum
        weighted_sum = self.calculate_weighted_sum(
            pairwise_matrix, criteria_values)

        # 4. Calculate the Priority Vector
        priority_vector = self.calculate_priority_vector(weighted_sum)

        # 5. Calculate the Consistency Ratio (optional)
        consistency_ratio = self.calculate_consistency_ratio(pairwise_matrix)

        # 6. Perform Sensitivity Analysis (optional)
        # Add sensitivity analysis logic if needed

        # 7. Generate the Final Ranking
        ranking = self.generate_final_ranking(priority_vector)

        # Create the AHP calculation instance with the calculated ranking and save it to the database
        ahp_calculation_data = {
            'supplier': supplier_id,
            'results': weighted_sum,
            'ranking': ranking,
        }
        serializer = self.get_serializer(data=ahp_calculation_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def calculate_weighted_sum(self, pairwise_matrix, criteria_values):
        weighted_sum = [0.0] * len(criteria_values)

        for i in range(len(criteria_values)):
            for j in range(len(pairwise_matrix[i])):
                weighted_sum[i] += pairwise_matrix[i][j] * criteria_values[j]

        return weighted_sum

    def calculate_priority_vector(self, weighted_sum):
        total_sum = sum(weighted_sum)
        priority_vector = [value / total_sum for value in weighted_sum]

        return priority_vector

    def calculate_consistency_ratio(self, pairwise_matrix):
        n = len(pairwise_matrix)

        # Calculate the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(pairwise_matrix)

        # Find the maximum eigenvalue
        max_eigenvalue = max(eigenvalues)

        # Calculate the consistency index
        consistency_index = (max_eigenvalue - n) / (n - 1)

        # Lookup random index (RI) value based on the size of the matrix
        random_index = self.get_random_index(n)

        # Calculate the consistency ratio
        consistency_ratio = consistency_index / random_index

        return consistency_ratio

    def get_random_index(self, n):
        random_index_table = {
            1: 0,
            2: 0,
            3: 0.58,
            4: 0.9,
            5: 1.12,
            6: 1.24,
            7: 1.32,
            8: 1.41,
            9: 1.45,
            10: 1.49,
            # Add more values if needed
        }

        return random_index_table.get(n, None)

    def generate_final_ranking(self, priority_vector):
        # Generate the final ranking by sorting the priority vector in descending order
        ranking = sorted(range(len(priority_vector)),
                         key=lambda i: priority_vector[i], reverse=True)

        return ranking


class AHPcalculationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AHPcalculation.objects.all()
    serializer_class = AHPcalculationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
