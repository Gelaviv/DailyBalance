from rest_framework import serializers
from .models import DailySchedule, DailyTask, ProgressStreak
from tasks.serializers import CategorySerializer

class DailyTaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = DailyTask
        fields = '__all__'
        read_only_fields = ('schedule', 'created_at', 'updated_at')
    
    def get_duration(self, obj):
        return obj.duration()


class DailyScheduleSerializer(serializers.ModelSerializer):
    daily_tasks = DailyTaskSerializer(many=True, read_only=True)
    completed_tasks_count = serializers.IntegerField(read_only=True)
    total_tasks_count = serializers.IntegerField(read_only=True)
    completion_percentage = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = DailySchedule
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class ProgressStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressStreak
        fields = '__all__'
        read_only_fields = ('user', 'last_updated')