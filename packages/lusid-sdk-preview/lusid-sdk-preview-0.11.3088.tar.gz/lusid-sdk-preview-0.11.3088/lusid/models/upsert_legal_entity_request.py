# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.3088
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class UpsertLegalEntityRequest(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'identifiers': 'dict(str, ModelProperty)',
        'properties': 'dict(str, ModelProperty)',
        'display_name': 'str',
        'description': 'str'
    }

    attribute_map = {
        'identifiers': 'identifiers',
        'properties': 'properties',
        'display_name': 'displayName',
        'description': 'description'
    }

    required_map = {
        'identifiers': 'required',
        'properties': 'optional',
        'display_name': 'required',
        'description': 'optional'
    }

    def __init__(self, identifiers=None, properties=None, display_name=None, description=None):  # noqa: E501
        """
        UpsertLegalEntityRequest - a model defined in OpenAPI

        :param identifiers:  The identifiers the legal entity will be upserted with.The provided keys should be idTypeScope, idTypeCode, code (required)
        :type identifiers: dict[str, lusid.ModelProperty]
        :param properties:  A set of properties associated to the Legal Entity.
        :type properties: dict[str, lusid.ModelProperty]
        :param display_name:  The display name of the Legal Entity (required)
        :type display_name: str
        :param description:  The description of the Legal Entity
        :type description: str

        """  # noqa: E501

        self._identifiers = None
        self._properties = None
        self._display_name = None
        self._description = None
        self.discriminator = None

        self.identifiers = identifiers
        self.properties = properties
        self.display_name = display_name
        self.description = description

    @property
    def identifiers(self):
        """Gets the identifiers of this UpsertLegalEntityRequest.  # noqa: E501

        The identifiers the legal entity will be upserted with.The provided keys should be idTypeScope, idTypeCode, code  # noqa: E501

        :return: The identifiers of this UpsertLegalEntityRequest.  # noqa: E501
        :rtype: dict(str, ModelProperty)
        """
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers):
        """Sets the identifiers of this UpsertLegalEntityRequest.

        The identifiers the legal entity will be upserted with.The provided keys should be idTypeScope, idTypeCode, code  # noqa: E501

        :param identifiers: The identifiers of this UpsertLegalEntityRequest.  # noqa: E501
        :type: dict(str, ModelProperty)
        """
        if identifiers is None:
            raise ValueError("Invalid value for `identifiers`, must not be `None`")  # noqa: E501

        self._identifiers = identifiers

    @property
    def properties(self):
        """Gets the properties of this UpsertLegalEntityRequest.  # noqa: E501

        A set of properties associated to the Legal Entity.  # noqa: E501

        :return: The properties of this UpsertLegalEntityRequest.  # noqa: E501
        :rtype: dict(str, ModelProperty)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this UpsertLegalEntityRequest.

        A set of properties associated to the Legal Entity.  # noqa: E501

        :param properties: The properties of this UpsertLegalEntityRequest.  # noqa: E501
        :type: dict(str, ModelProperty)
        """

        self._properties = properties

    @property
    def display_name(self):
        """Gets the display_name of this UpsertLegalEntityRequest.  # noqa: E501

        The display name of the Legal Entity  # noqa: E501

        :return: The display_name of this UpsertLegalEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this UpsertLegalEntityRequest.

        The display name of the Legal Entity  # noqa: E501

        :param display_name: The display_name of this UpsertLegalEntityRequest.  # noqa: E501
        :type: str
        """
        if display_name is None:
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501
        if display_name is not None and len(display_name) > 512:
            raise ValueError("Invalid value for `display_name`, length must be less than or equal to `512`")  # noqa: E501
        if display_name is not None and len(display_name) < 1:
            raise ValueError("Invalid value for `display_name`, length must be greater than or equal to `1`")  # noqa: E501
        if (display_name is not None and not re.search(r'(?s).*', display_name)):  # noqa: E501
            raise ValueError(r"Invalid value for `display_name`, must be a follow pattern or equal to `/(?s).*/`")  # noqa: E501

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this UpsertLegalEntityRequest.  # noqa: E501

        The description of the Legal Entity  # noqa: E501

        :return: The description of this UpsertLegalEntityRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpsertLegalEntityRequest.

        The description of the Legal Entity  # noqa: E501

        :param description: The description of this UpsertLegalEntityRequest.  # noqa: E501
        :type: str
        """
        if description is not None and len(description) > 512:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `512`")  # noqa: E501
        if description is not None and len(description) < 0:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501
        if (description is not None and not re.search(r'(?s).*', description)):  # noqa: E501
            raise ValueError(r"Invalid value for `description`, must be a follow pattern or equal to `/(?s).*/`")  # noqa: E501

        self._description = description

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
        if not isinstance(other, UpsertLegalEntityRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
