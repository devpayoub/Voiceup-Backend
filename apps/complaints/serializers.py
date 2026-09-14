from rest_framework import serializers

from .models import Category, Comment, Company, Complaint, Region


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'sector', 'verified']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'complaint', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'complaint', 'user', 'created_at']


class ComplaintSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    company_name = serializers.CharField(write_only=True, max_length=200)
    backer_count = serializers.IntegerField(source='backers.count', read_only=True)
    comment_count = serializers.SerializerMethodField()
    is_backed_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [
            'id', 'user', 'company', 'company_name', 'category', 'title', 'description',
            'photo', 'region', 'city', 'status', 'created_at', 'updated_at',
            'backer_count', 'comment_count', 'is_backed_by_me',
        ]
        read_only_fields = ['id', 'user', 'company', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        name = validated_data.pop('company_name').strip()
        company = Company.objects.filter(name__iexact=name).first()
        if not company:
            company = Company.objects.create(name=name)
        validated_data['company'] = company
        return super().create(validated_data)

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_backed_by_me(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.backers.filter(user=request.user).exists()
