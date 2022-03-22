from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions, serializers

from dora.rest_auth.models import Token
from dora.structures.emails import send_invitation_email
from dora.users.models import User

from .models import (
    Structure,
    StructureMember,
    StructurePutativeMember,
    StructureTypology,
)


class StructureSerializer(serializers.ModelSerializer):
    typology = serializers.SlugRelatedField(
        slug_field="value", queryset=StructureTypology.objects.all()
    )
    typology_display = serializers.SerializerMethodField()
    parent = serializers.SlugRelatedField(
        queryset=Structure.objects.all(), slug_field="slug"
    )
    can_write = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = [
            "siret",
            "code_safir_pe",
            "typology",
            "typology_display",
            "slug",
            "name",
            "short_desc",
            "url",
            "full_desc",
            "phone",
            "email",
            "postal_code",
            "city_code",
            "city",
            "department",
            "address1",
            "address2",
            "ape",
            "longitude",
            "latitude",
            "creation_date",
            "modification_date",
            "can_write",
            "is_admin",
            "is_member",
            "parent",
        ]
        lookup_field = "slug"

    def get_can_write(self, obj):
        # TODO: DEPRECATED
        user = self.context.get("request").user
        return obj.can_write(user)

    def get_is_member(self, obj):
        user = self.context.get("request").user
        return obj.is_member(user)

    def get_is_admin(self, obj):
        user = self.context.get("request").user
        return obj.is_admin(user)

    def get_typology_display(self, obj):
        return obj.typology.label if obj.typology else ""


class StructureListSerializer(StructureSerializer):
    # num_services = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = [
            "slug",
            "name",
            "department",
            "typology_display",
            "modification_date",
            "parent"
            # "num_services"
        ]
        lookup_field = "slug"

    # def get_num_services(self, obj):
    #     return obj.services.count()


class SiretClaimedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ["siret", "slug"]
        lookup_field = "siret"


class UserSerializer(serializers.ModelSerializer):
    # We want to suppress the unique constraint validation here
    # as we might get passed an existing user email on creation
    email = serializers.EmailField(label="Email address", max_length=255, validators=[])
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "full_name", "email"]


class StructureMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StructureMember
        fields = [
            "id",
            "user",
            "is_admin",
        ]
        validators = []

    def validate(self, data):
        structure_slug = self.context["request"].query_params.get("structure")
        if structure_slug:
            try:
                structure = Structure.objects.get(slug=structure_slug)
            except Structure.DoesNotExist:
                raise exceptions.NotFound
            data["structure"] = structure
        return data

    def update(self, instance, validated_data):
        # For now, we don't want the user to be editable this way
        # user_data = validated_data.pop("user") if "user" in validated_data else {}
        # user = instance.user
        # for attr, value in user_data.items():
        #     setattr(user, attr, value)
        # user.save()

        if "user" in validated_data:
            validated_data.pop("user")
        if instance.is_admin and validated_data.get("is_admin") is False:
            request_user = self.context["request"].user
            if not request_user.is_staff:
                # Only remove admin status if there's at least another one
                num_admins = StructureMember.objects.filter(
                    structure=instance.structure, is_admin=True
                ).count()
                if num_admins == 1:
                    raise exceptions.PermissionDenied
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StructurePutativeMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    must_set_password = serializers.SerializerMethodField()

    class Meta:
        model = StructurePutativeMember
        fields = [
            "id",
            "user",
            "is_admin",
            "must_set_password",
            "invited_by_admin",
        ]
        validators = []

    def get_must_set_password(self, obj):
        return not obj.user.has_usable_password()

    def validate(self, data):
        structure_slug = self.context["request"].query_params.get("structure")
        if structure_slug:
            try:
                structure = Structure.objects.get(slug=structure_slug)
            except Structure.DoesNotExist:
                raise exceptions.NotFound
            data["structure"] = structure
        return data

    def create(self, validated_data):
        request_user = self.context["request"].user
        user_data = validated_data.pop("user")
        try:
            user = User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            # TODO: use create_user instead
            user = User.objects.create(**user_data)
            user.set_unusable_password()
            user.save()
        try:
            StructurePutativeMember.objects.get(
                user=user, structure=validated_data["structure"]
            )
            raise exceptions.PermissionDenied
        except StructurePutativeMember.DoesNotExist:
            pass
        member = StructurePutativeMember.objects.create(
            user=user,
            **validated_data,
            invited_by_admin=True,
        )
        # Send invitation email
        tmp_token = Token.objects.create(
            user=user, expiration=timezone.now() + settings.INVITATION_LINK_EXPIRATION
        )
        send_invitation_email(
            member,
            request_user.get_full_name(),
            tmp_token.key,
        )
        return member
