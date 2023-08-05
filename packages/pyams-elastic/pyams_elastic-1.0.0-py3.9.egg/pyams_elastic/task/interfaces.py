#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_elastic.task.interfaces module

This module defines interface of PyAMS_elastic scheduler task,
which can be used to handle Elasticsearch regular queries.
"""

from zope.interface import Interface, Invalid, invariant
from zope.schema import Object, Text, TextLine

from pyams_elastic.interfaces import IElasticClientInfo
from pyams_scheduler.interfaces import ITask
from pyams_utils.schema import TextLineListField


__docformat__ = 'restructuredtext'

from pyams_elastic import _  # pylint: disable=ungrouped-imports


class IElasticTaskInfo(Interface):
    """Elasticsearch scheduler task interface"""

    connection = Object(title=_("Elasticsearch connection"),
                        schema=IElasticClientInfo,
                        required=True)

    query = Text(title=_("Query"),
                 description=_("Complete Elasticsearch query, in JSON format"),
                 required=True)

    expected_results = TextLine(title=_("Expected results count"),
                                description=_("Number of expected results; you can enter a "
                                              "single number, or a range by entering two "
                                              "numbers separated by a dash; an error status "
                                              "will be returned if the number of results is "
                                              "not in the given range; if the input is left "
                                              "empty, all queries will return an error"),
                                required=False)

    @invariant
    def check_expected_results(self):
        """Check format of expected results entry"""
        expected = self.expected_results
        if expected:
            try:
                if '-' in expected:  # pylint: disable=unsupported-membership-test
                    mini, maxi = map(int, expected.split('-'))  # pylint: disable=no-member
                    if mini > maxi:
                        raise ValueError("Minimum value must be lower or equal to maximum value")
                else:
                    _value = int(expected)
            except ValueError as exc:
                raise Invalid(_("Expected results must be a single positive number, or two "
                                "positive numbers separated by a dash")) from exc

    log_fields = TextLineListField(title=_("Log output fields"),
                                   description=_("List of results fields to include in task "
                                                 "log output report"),
                                   required=False)


class IElasticTask(ITask, IElasticTaskInfo):
    """Elasticsearch task interface"""
