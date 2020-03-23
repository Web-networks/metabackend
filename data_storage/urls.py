from django.urls import path, include
from . import models
from rest_framework import routers, serializers, viewsets


class NeuralModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.NeuralModel
        fields = ['id', 'user_id', 'execution_code_url']


class NeuralModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.NeuralModel.objects.all()
    serializer_class = NeuralModelSerializer


class UserInputSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserInput
        fields = ['id', 'user_id', 'data_url']


class UserInputViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.UserInput.objects.all()
    serializer_class = UserInputSerializer


class TrainingTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TrainingTask
        fields = ['id', 'user_id', 'model', 'user_input', 'parameters', 'status', 'error_message', 'result_url']


class TrainingTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TrainingTask.objects.all()
    serializer_class = TrainingTaskSerializer


router = routers.DefaultRouter()
router.register(r'neural-models', NeuralModelViewSet)
router.register(r'user-input', UserInputViewSet)
router.register(r'taining-tasks', TrainingTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
