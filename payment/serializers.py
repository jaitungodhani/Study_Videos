from rest_framework import serializers

class CreateCheckoutSessionSerializer(serializers.Serializer):
    lookup_key = serializers.CharField()
    success_url = serializers.CharField()
    cancel_url = serializers.CharField()

