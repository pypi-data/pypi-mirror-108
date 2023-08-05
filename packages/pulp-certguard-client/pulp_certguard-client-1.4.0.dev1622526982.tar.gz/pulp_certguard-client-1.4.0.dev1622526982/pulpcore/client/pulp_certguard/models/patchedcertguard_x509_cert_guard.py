# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_certguard.configuration import Configuration


class PatchedcertguardX509CertGuard(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'description': 'str',
        'ca_certificate': 'str'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'ca_certificate': 'ca_certificate'
    }

    def __init__(self, name=None, description=None, ca_certificate=None, local_vars_configuration=None):  # noqa: E501
        """PatchedcertguardX509CertGuard - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._ca_certificate = None
        self.discriminator = None

        if name is not None:
            self.name = name
        self.description = description
        if ca_certificate is not None:
            self.ca_certificate = ca_certificate

    @property
    def name(self):
        """Gets the name of this PatchedcertguardX509CertGuard.  # noqa: E501

        The unique name.  # noqa: E501

        :return: The name of this PatchedcertguardX509CertGuard.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PatchedcertguardX509CertGuard.

        The unique name.  # noqa: E501

        :param name: The name of this PatchedcertguardX509CertGuard.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this PatchedcertguardX509CertGuard.  # noqa: E501

        An optional description.  # noqa: E501

        :return: The description of this PatchedcertguardX509CertGuard.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PatchedcertguardX509CertGuard.

        An optional description.  # noqa: E501

        :param description: The description of this PatchedcertguardX509CertGuard.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def ca_certificate(self):
        """Gets the ca_certificate of this PatchedcertguardX509CertGuard.  # noqa: E501

        The Certificate Authority (CA) certificate.  # noqa: E501

        :return: The ca_certificate of this PatchedcertguardX509CertGuard.  # noqa: E501
        :rtype: str
        """
        return self._ca_certificate

    @ca_certificate.setter
    def ca_certificate(self, ca_certificate):
        """Sets the ca_certificate of this PatchedcertguardX509CertGuard.

        The Certificate Authority (CA) certificate.  # noqa: E501

        :param ca_certificate: The ca_certificate of this PatchedcertguardX509CertGuard.  # noqa: E501
        :type: str
        """

        self._ca_certificate = ca_certificate

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PatchedcertguardX509CertGuard):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatchedcertguardX509CertGuard):
            return True

        return self.to_dict() != other.to_dict()
