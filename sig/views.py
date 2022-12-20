from sig.models import Sig, SigParsed, SigReviewed
from django.contrib.auth.models import User
from django.db.models import Count
from sig.serializers import SigSerializer, SigParsedSerializer, SigReviewedSerializer, UserSerializer
from sig.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from rest_framework.decorators import action
from parsers.sig import SigParser
import csv

class SigViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`,
    and `destroy` actions.
    It does not provide `update` actions.
    """
    # TODO: API key users should only be able to create, not to list, retrieve, or destroy
    permission_classes = [HasAPIKey | IsAuthenticated]
    serializer_class = SigSerializer
    queryset = Sig.objects.all()

    def get_queryset(self):
        queryset = Sig.objects.all()
        
        reviewed = self.request.query_params.get('reviewed', None)
        if reviewed is not None:
            reviewed = int(reviewed)
            queryset = queryset.annotate(sig_reviewed_count=Count('sig_parsed__sig_reviewed'))
            if reviewed == 1:
                # if we want reviewed sigs, we want sigs that have at least one review, AND which have been reviewed by the current user
                # technically, we probably don't even need the count greater than 0 if we have one review from current user
                # order by the most recent review date descending
                queryset = queryset.filter(sig_reviewed_count__gt=0, sig_parsed__sig_reviewed__owner=self.request.user).order_by('-sig_parsed__sig_reviewed__created').distinct()
            elif reviewed == 0:
                # if we want unreviewed sigs, we want sigs that have fewer than 2 reviews, AND which have not been reviewed by the current user
                queryset = queryset.filter(sig_reviewed_count__lt=2).distinct()
                queryset = queryset.exclude(sig_parsed__sig_reviewed__owner=self.request.user)
        
        sig_correct = self.request.query_params.get('sig_correct', None)
        if sig_correct is not None:
            sig_correct = int(sig_correct)
            queryset = queryset.filter(sig_parsed__sig_reviewed__sig_correct=sig_correct).order_by('-sig_parsed__sig_reviewed__created').distinct()
        
        dose = self.request.query_params.get('dose', None)
        if dose is not None:
            dose = int(dose)
            queryset = queryset.filter(sig_parsed__dose=dose)
        
        dose_unit = self.request.query_params.get('dose_unit', None)
        if dose_unit is not None:
            dose_unit = None if dose_unit == '' else dose_unit                
            queryset = queryset.filter(sig_parsed__dose_unit=dose_unit)
        
        strength_unit = self.request.query_params.get('strength_unit', None)
        if strength_unit is not None:
            strength_unit = None if strength_unit == '' else strength_unit                
            queryset = queryset.filter(sig_parsed__strength_unit=strength_unit)

        return queryset

    def create(self, request, *args, **kwargs):
        original_sig_text = request.data['sig_text']
        sig_text = SigParser().get_normalized_sig_text(original_sig_text)
        ndc = request.data['ndc'] if 'ndc' in request.data.keys() and request.data['ndc'].isnumeric() else None
        rxcui = request.data['rxcui'] if 'rxcui' in request.data.keys() and request.data['rxcui'].isnumeric() else None
        sigs = Sig.objects.filter(sig_text=sig_text)

        # if sig does NOT exist, parse the new sig
        if not sigs:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # if user is staff, return all sig_parsed
            # else, return optimal sig_parsed (for customers)
            sig = serializer.data if request.user.is_staff else self.replace_sig_parsed_optimal(serializer.data)
            if ndc or rxcui:
                sig_parsed = sig['sig_parsed'][0] if type(sig['sig_parsed']) is list else sig['sig_parsed']
                sig['sig_inferred'] = self.get_sig_inferred(sig_parsed, ndc=ndc, rxcui=rxcui)
            sig['original_sig_text'] = original_sig_text
            return Response(sig, status=status.HTTP_201_CREATED, headers=headers)
        # if sig DOES exist...
        else:

            # TODO: if sig has no sig_parsed with a sig_reviewed, return most recent parsed_sig with a disclaimer
            # TODO: if sig has at least one sig_parsed...
            # TODO: if at least one sig_parsed has a positive review, return the most recent version reviewed
            # TODO: if at least one sig_parsed is unreviewed, return the most recent unreviewed version with a disclaimer
            # TODO: if all sig_parsed versions have negative reviews, return error OR return negatively reviewed sig with huge disclaimer
            # ...return the existing parsed sig
            serializer = self.get_serializer(sigs[0])
            # if user is staff, return all sig_parsed
            # else, return optimal sig_parsed (for customers)
            sig = serializer.data if request.user.is_staff else self.replace_sig_parsed_optimal(serializer.data)
            if ndc or rxcui:
                sig_parsed = sig['sig_parsed'][0] if type(sig['sig_parsed']) is list else sig['sig_parsed']
                sig['sig_inferred'] = self.get_sig_inferred(sig_parsed, ndc=ndc, rxcui=rxcui)
            sig['original_sig_text'] = original_sig_text
            return Response(sig)

    def get_sig_inferred(self, sig_parsed, ndc=None, rxcui=None):
        sig_inferred_data = SigParser().infer(sig_parsed, ndc, rxcui)
        return sig_inferred_data

    def replace_sig_parsed_optimal(self, sig):
        # sig_parsed is sorted by created descending, so most recent are at top of list
        # first, check for first (most recent) sig_parsed with sig_reviewed_status == 'correct'
        # if no 'correct' sig_reviewed, then just return the most recent sig_parsed
        # user can see sig_reviewed_status in results and make judgement
        sig_parsed = sig['sig_parsed']
        sig_parsed_reviewed_correct = next((sp for sp in sig_parsed if sp['sig_reviewed_status'] == 'correct'), None)
        sig['sig_parsed'] = sig_parsed_reviewed_correct if sig_parsed_reviewed_correct is not None else sig_parsed[0]
        return sig

# TODO: eventually combine this into SigViewSet after testing
class BulkSigCreateViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    This viewset provides a bulk `create`, action.
    """
    queryset = Sig.objects.all()
    serializer_class = SigSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        
        # I think this is where I would check for existing reviews
        # NOTE: existing sigs are checked in the get_or_create method of SigSerializer

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
        )

        # TODO: if sig has no sig_parsed with a sig_reviewed, return most recent parsed_sig with a disclaimer
        # TODO: if sig has at least one sig_parsed...
        # TODO: if at least one sig_parsed has a positive review, return the most recent version reviewed
        # TODO: if at least one sig_parsed is unreviewed, return the most recent unreviewed version with a disclaimer
        # TODO: if all sig_parsed versions have negative reviews, return error OR return negatively reviewed sig with huge disclaimer
        # ...return the existing parsed sig

class CsvSigCreateViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    This viewset provides a bulk `create`, action for sigs in a csv.
    """
    queryset = Sig.objects.all()
    serializer_class = SigSerializer
    def create(self, request, *args, **kwargs):
        # NOTE: I have several different sizes of csv in the parsers/csv folder
        # 10, 100, 250, 500, 1000, and all 23000+ (sig.csv)
        filepath = 'parsers/csv/drx_current.csv'

        with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            data = [{'sig_text': row[0]} for row in csv_reader]

        print(data)
        
        # I think this is where I would check for existing reviews
        # NOTE: existing sigs are checked in the get_or_create method of SigSerializer

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #print(serializer.data)
        return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
        )

        # TODO: if sig has no sig_parsed with a sig_reviewed, return most recent parsed_sig with a disclaimer
        # TODO: if sig has at least one sig_parsed...
        # TODO: if at least one sig_parsed has a positive review, return the most recent version reviewed
        # TODO: if at least one sig_parsed is unreviewed, return the most recent unreviewed version with a disclaimer
        # TODO: if all sig_parsed versions have negative reviews, return error OR return negatively reviewed sig with huge disclaimer
        # ...return the existing parsed sig


class SigReviewedViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = SigReviewed.objects.all()
    serializer_class = SigReviewedSerializer
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        many = isinstance(data, list)
        print (data, many)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
        )

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer