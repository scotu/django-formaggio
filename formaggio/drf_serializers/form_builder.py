from rest_framework import serializers
from ..models import FormaggioForm, FormaggioField

class FormaggioFormReadSerializer(serializers.ModelSerializer):
    fields = FormaggioFieldReadSerializer(many=True, read_only=True)
    class Meta:
        model = FormaggioForm
        fields = (
            'title',
            'fields',
        )

class FormaggioFieldReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaggioField
        fields = (
            'title',
            'fields',
        )
