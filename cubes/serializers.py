from rest_framework import serializers
from .models import Cube

class BoxSerializers(serializers.ModelSerializer):
    #only username should be there  not id and object in response
    created_by = serializers.ReadOnlyField(source="created_by.username")

    #for removing the extra field for normal user
    def to_representation(self, instance):
        rep = super(BoxSerializers, self).to_representation(instance)
        request = self.context.get("request")
        if not request.user.is_staff:
            rep.pop("created_by")
            rep.pop("last_updated")
        # it will remove the date of creations from the response
        rep.pop("date_of_creation")
        return rep
    class Meta:
        model = Cube
        fields = '__all__'