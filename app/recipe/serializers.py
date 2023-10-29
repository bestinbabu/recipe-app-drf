from rest_framework import serializers
from core.models import Recipe,Tag,Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
        

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link','tags')
        read_only_fields = ('id',)
    
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        ingredients_data = validated_data.pop('ingredients')
        auth_user = self.context['request'].user
        for tag_data in tags_data:
            tag = Tag.objects.create(user=auth_user, **tag_data)
            recipe.tags.add(tag)
            
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.create(user=auth_user, **ingredient_data)
            recipe.ingredients.add(ingredient)
            
        return recipe
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        instance.ingredients.clear()
        instance.tags.clear()
        for tag_data in tags_data:
            tag = Tag.objects.create(user=self.context['request'].user, **tag_data)
            instance.tags.add(tag)
        
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.create(user=self.context['request'].user, **ingredient_data)
            instance.ingredients.add(ingredient)
        
        return super().update(instance, validated_data)
        
        

class RecipeDetailSerializer(RecipeSerializer):
    
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
        

