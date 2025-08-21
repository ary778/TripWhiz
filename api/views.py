from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from travel.models import Deal, Destination
from .serializers import DealSerializer
from travel.utils import fetch_and_store_deals_from_serpapi

class DealListView(ListAPIView):
    serializer_class = DealSerializer

    def get_queryset(self):
        queryset = Deal.objects.all()
        source = self.request.query_params.get('source')
        budget = self.request.query_params.get('budget')
        category = self.request.query_params.get('category')

        if source:
            queryset = queryset.filter(
                Q(origin_iata__iexact=source) | Q(origin_name__iexact=source)
            )
        if budget:
            try:
                queryset = queryset.filter(total_price__lte=int(budget))
            except (ValueError, TypeError): pass
        if category:
            queryset = queryset.filter(destination__category__iexact=category)
        
        return queryset.order_by('destination__name', 'total_price').distinct('destination__name')[:10]

    def list(self, request, *args, **kwargs):
        source_query = request.query_params.get('source')
        category_query = request.query_params.get('category')
        if not source_query:
            return Response({"error": "A source city or IATA code is required."}, status=400)

        existing_deals = self.get_queryset()

        if not existing_deals.exists():
            print(f"No deals found for '{source_query}'. Attempting to fetch from SerpAPI...")
            
            source_iata_to_search = None
            # Find the destination object for the source to get its IATA code
            source_destination_obj = Destination.objects.filter(
                Q(iata_code__iexact=source_query) | Q(name__iexact=source_query)
            ).first()

            if source_destination_obj:
                source_iata_to_search = source_destination_obj.iata_code
                print(f"Found source '{source_destination_obj.name}' in database. Using IATA code: {source_iata_to_search}")
                # Pass the reliable IATA code to the fetcher function
                fetch_and_store_deals_from_serpapi(source_iata_to_search, category_query)
            else:
                # If the source itself is unknown, we cannot make a reliable API call
                print(f"Source city '{source_query}' is not in the Destination database. Cannot fetch new deals.")
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)