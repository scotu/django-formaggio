from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from ..models import FormaggioFormResult
from ..drf_serializers.form_answer import FormaggioFormResultSerializer


class FormAnswerViewSet(CreateModelMixin, GenericViewSet):
    queryset = FormaggioFormResult.objects.all()
    serializer_class = FormaggioFormResultSerializer
