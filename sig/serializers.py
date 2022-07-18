from rest_framework import serializers
from sig.models import Sig, SigParsed, SigReviewed
from parsers.sig import SigParser
from django.contrib.auth.models import User
from django.db import transaction

class SigReviewedSerializer(serializers.ModelSerializer):
    sig_parsed = serializers.PrimaryKeyRelatedField(queryset=SigParsed.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        # NOTE: this is how we only show reviews that were completed by the currently logged in user
        model = SigReviewed
        fields = ['id', 'created', 'sig_parsed', 'owner', 'sig_correct', 'method_status', 'dose_status', 'strength_status', 'route_status', 'frequency_status', 'duration_status', 'indication_status', 'themes', 'notes']

class SigParsedSerializer(serializers.ModelSerializer):
    sig_reviewed = SigReviewedSerializer(many=True, read_only=True)
    sig_reviewed_status = serializers.SerializerMethodField()

    class Meta:
        model = SigParsed
        fields = ['id', 'sig_text', 'sig_readable', 'created', 'version', 'method', 'dose', 'dose_max', 'dose_unit', 'strength', 'strength_max', 'strength_unit', 'route', 'frequency', 'frequency_max', 'period', 'period_max', 'period_unit', 'time_duration', 'time_duration_unit', 'day_of_week', 'time_of_day', 'when', 'offset', 'bounds', 'count', 'duration', 'duration_max', 'duration_unit', 'as_needed', 'indication', 'sig_reviewed', 'sig_reviewed_status'
        ,'method_text', 'method_text_start', 'method_text_end', 'method_readable', 'dose_text', 'dose_text_start', 'dose_text_end', 'dose_readable', 'strength_text', 'strength_text_start', 'strength_text_end', 'strength_readable', 'route_text', 'route_text_start', 'route_text_end', 'route_readable', 'frequency_text', 'frequency_text_start', 'frequency_text_end', 'frequency_readable', 'when_text', 'when_text_start', 'when_text_end', 'when_readable', 'duration_text', 'duration_text_start', 'duration_text_end', 'duration_readable', 'indication_text', 'indication_text_start', 'indication_text_end', 'indication_readable', 'max_numerator_value', 'max_numerator_unit', 'max_denominator_value', 'max_denominator_unit', 'max_text_start', 'max_text_end', 'max_text', 'max_readable']

    def get_sig_reviewed_status(self, obj):
        if not hasattr(obj, 'id'):
            # if we are using GET on a sig that doesn't exist in database, we parse it and don't assign an ID
            # so the sig is technically 'unreviewed'
            return 'unreviewed'

        q = SigReviewed.objects.filter(sig_parsed_id__exact=obj.id)
        total_count = q.count()
        correct_count = q.filter(sig_correct__exact=1).count()
        incorrect_count = q.filter(sig_correct__exact=0).count()
        if incorrect_count == 0 and correct_count > 0:
            return 'correct'
        elif incorrect_count > 0:
            return 'incorrect'
        elif total_count == 0:
            return 'unreviewed'
        else:
            return 'unknown'
        
class BulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            result = [self.child.create(attrs) for attrs in validated_data]

        return result

# NOTE: went down the path of bulk_create - since it doesn't return pk and save() prevents saving child without parent pk, it doesn't work
#       postgreSQL would fix this, but is a pain because DreamHost doesn't support
class SigSerializer(serializers.ModelSerializer):
    sig_parsed = SigParsedSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    
    def create(self, validated_data):
        sig_text = validated_data['sig_text']
        sig_parsed_data = SigParser().parse(sig_text)
        # if someone submits a sig of "TAKE 1  TABLET DAILY", we want the sig parser to normalize it to "take 1 tablet daily"
        # sig parser gets rid of duplicate spaces, lower cases sig, and trims whitespace at beginning and end
        # fall back to original sig_text just in case something goes wrong with parser
        validated_data['sig_text'] = sig_parsed_data['sig_text'] if sig_parsed_data['sig_text'] else sig_text
        sig, _ = Sig.objects.get_or_create(**validated_data)
        sig_parsed, _ = SigParsed.objects.get_or_create(sig=sig, version=0, **sig_parsed_data) # TODO: probably move version creation to SigParserSerializer and make it actually do something
        return sig

    class Meta:
        model = Sig
        fields = ['id', 'sig_text', 'owner', 'sig_parsed']
        list_serializer_class = BulkCreateListSerializer

class UserSerializer(serializers.ModelSerializer):
    sigs = serializers.HyperlinkedRelatedField(many=True, view_name='sig-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'sigs']