#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.HyperLinkedNodelSerializer):
    """
    Serializes and Deserializes User instances into representations such as 
    JSON.
    """
    class Meta:
        """
        Fields of User instances that will get serialized/deserialized.
        """
        model = get_user_model()
        fields = ('username', 'date_joined')
