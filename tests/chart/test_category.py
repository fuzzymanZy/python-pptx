# encoding: utf-8

"""
Unit test suite for the pptx.chart.category module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from pptx.chart.category import Categories, Category

from ..unitutil.cxml import element
from ..unitutil.mock import call, class_mock, instance_mock


class DescribeCategories(object):

    def it_knows_its_length(self, len_fixture):
        categories, expected_len = len_fixture
        assert len(categories) == expected_len

    def it_supports_indexed_access(self, getitem_fixture):
        categories, idx, Category_, pt, category_ = getitem_fixture
        category = categories[idx]
        Category_.assert_called_once_with(pt, idx)
        assert category is category_

    def it_can_iterate_over_the_categories_it_contains(self, iter_fixture):
        categories, expected_categories, Category_, calls, = iter_fixture
        assert [c for c in categories] == expected_categories
        assert Category_.call_args_list == calls

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('c:barChart/c:ser/c:cat/(c:ptCount{val=2},c:pt{idx=1})', 1, 0),
        ('c:barChart/c:ser/c:cat/(c:ptCount{val=2},c:pt{idx=1})', 0, None),
    ])
    def getitem_fixture(self, request, Category_, category_):
        xChart_cxml, idx, pt_offset = request.param
        xChart = element(xChart_cxml)
        pt = None if pt_offset is None else xChart.xpath('.//c:pt')[pt_offset]
        categories = Categories(xChart)
        return categories, idx, Category_, pt, category_

    @pytest.fixture
    def iter_fixture(self, Category_, category_):
        xChart = element(
            'c:barChart/c:ser/c:cat/(c:ptCount{val=2},c:pt{idx=1})'
        )
        pt = xChart.xpath('.//c:pt')[0]
        categories = Categories(xChart)
        expected_categories = [category_, category_]
        calls = [call(None, 0), call(pt, 1)]
        return categories, expected_categories, Category_, calls

    @pytest.fixture(params=[
        ('c:barChart', 0),
        ('c:barChart/c:ser/c:cat/c:ptCount{val=4}', 4),
    ])
    def len_fixture(self, request):
        xChart_cxml, expected_len = request.param
        categories = Categories(element(xChart_cxml))
        return categories, expected_len

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Category_(self, request, category_):
        return class_mock(
            request, 'pptx.chart.category.Category', return_value=category_
        )

    @pytest.fixture
    def category_(self, request):
        return instance_mock(request, Category)