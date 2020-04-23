from django.urls import path, include
from . import models
from rest_framework import routers, serializers, viewsets


class NeuralModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.NeuralModel
        fields = '__all__'


class NeuralModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.NeuralModel.objects.all()
    serializer_class = NeuralModelSerializer


class UserInputSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserInput
        fields = '__all__'


class UserInputViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.UserInput.objects.all()
    serializer_class = UserInputSerializer


class TrainingTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TrainingTask
        fields = '__all__'


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
