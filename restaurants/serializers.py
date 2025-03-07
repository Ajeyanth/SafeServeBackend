from rest_framework import serializers
from .models import Restaurant, MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class MenuItemSerializer(serializers.ModelSerializer):
    # For reading, show nested category; for writing, accept category_id.
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True,
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'ingredients', 'allergens', 'category', 'category_id', 'last_updated', 'restaurant']
        read_only_fields = ['last_updated', 'restaurant']

    def validate(self, data):
        # Get the restaurant from the serializer context (set in the view)
        restaurant = self.context.get('restaurant')
        category = data.get('category')
        if category and restaurant and category.restaurant != restaurant:
            raise serializers.ValidationError({"category_id": "Category does not belong to this restaurant."})
        return data

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'location', 'cuisine_type', 'last_updated', 'menu_items']
        read_only_fields = ['owner']
