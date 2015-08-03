from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, fromstr
from django.core import cache as django_cache
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import (views, permissions, mixins, authentication,
                            generics, exceptions, status)
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from rest_framework_bulk import generics as bulk_generics
from social.apps.django_app import views as social_views
from mock import patch
from .. import apikey
from .. import cors
from .. import models
from .. import serializers
from .. import utils
from .. import renderers
from .. import parsers
from .. import apikey
from .. import cors
from .. import tasks
from .. import utils
from ..cache import cache_buffer
from ..params import (INCLUDE_INVISIBLE_PARAM, INCLUDE_PRIVATE_PARAM,
    INCLUDE_SUBMISSIONS_PARAM, NEAR_PARAM, DISTANCE_PARAM, BBOX_PARAM,
    TEXTSEARCH_PARAM, FORMAT_PARAM, PAGE_PARAM, PAGE_SIZE_PARAM,
    CALLBACK_PARAM)
from functools import wraps
from itertools import groupby, count
from collections import defaultdict
from urllib import urlencode
import re
import requests
import ujson as json
import logging

logger = logging.getLogger('sa_api_v2.views')


###############################################################################
#
# Content Negotiation
# -------------------
#


def bulk(request="none"):
	place = models.core.Place()
	place.dataset_id = '1'
	place.submitter_id = '1'
	my_lat = '33.755787'
	my_long = '-116.359998'
	place.geometry = fromstr('POINT(' + my_long + ' ' + my_lat + ')')
	place.data = '{"private-submitter_email":"test","name":"test","user_token":"session:842e0c2fb637edb9787cb0678a16016d","hint_category":"improvement","location":{"sideOfStreet":"N","linkId":"0","mapUrl":"http:\/\/open.mapquestapi.com\/staticmap\/v4\/getmap?key=Fmjtd|luur2g0bnl,25=o5-9at29u&type=map&size=225,160&pois=purple-1,37.3440744,-121.8864022,0,0,|&center=37.3440744,-121.8864022&zoom=15&rand=860370430","displayLatLng":{"lat":37.344074,"lng":-121.886402},"adminArea6Type":"Neighborhood","adminArea3Type":"State","dragPoint":false,"geocodeQualityCode":"B1AAA","adminArea1":"US","geocodeQuality":"STREET","adminArea3":"CA","adminArea4":"Santa Clara County","adminArea5":"San Jos\u00e9","adminArea6":"","postalCode":"95112","type":"s","adminArea1Type":"Country","adminArea5Type":"City","latLng":{"lat":37.344074,"lng":-121.886402},"adminArea4Type":"County","unknownInput":"","street":"North 8th Street"},"submitter_name":"test","location_type":"side_walk","description":"test"}';
	place.save()

	return HttpResponse("Hello, world. You're at the polls index.")