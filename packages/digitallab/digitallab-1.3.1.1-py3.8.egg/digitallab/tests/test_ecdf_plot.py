#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from unittest import TestCase
import importlib


class MockSingleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        return self._decorated()


import digitallab.helper.db_access


@MockSingleton
class MockDBAccess:
    def connect(self, mongodb_url, mongodb_db, keys_json_path: str, cache_id: str = "default"):
        self.is_connected = True

    def get_dataframe(self):
        return pd.read_csv("mock_data.csv")


digitallab.helper.db_access.DBAccess = MockDBAccess

import pandas as pd
from digitallab.evaluation.plots.ecdf_plot import ECDFPlot


class TestECDFPlot(TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        importlib.reload(digitallab.helper.db_access)

    def test_plot_shows_without_errors(self):
        ECDFPlot("test"). \
            set_methods_key("method", "Method"). \
            set_value_of_interest("runtime", "Run time in seconds"). \
            add_unit_to_compare("Low", method="low"). \
            add_unit_to_compare("High", method="high"). \
            filter_data(prop1="a", prop2="a"). \
            set_yaxis_label("Proportion of solved instances"). \
            set_font_scale(1). \
            set_save_fig_size("a3"). \
            plot()

    def test_plot_order_does_not_matter(self):
        ECDFPlot("test"). \
            set_methods_key("method", "Method"). \
            set_value_of_interest("runtime", "Run time in seconds"). \
            add_unit_to_compare("High", method="high"). \
            add_unit_to_compare("Low", method="low"). \
            filter_data(prop1="a", prop2="a"). \
            set_yaxis_label("Proportion of solved instances"). \
            set_font_scale(1). \
            set_save_fig_size("a3"). \
            plot()

    def test_grid_works_without_errors(self):
        ECDFPlot("test"). \
            set_methods_key("method", "Method"). \
            set_value_of_interest("runtime", "Run time in seconds"). \
            add_unit_to_compare("High", method="high"). \
            add_unit_to_compare("Low", method="low"). \
            add_grid("prop1", "prop2", col_label="Property 1", row_label="Property 2"). \
            set_yaxis_label("Proportion of solved instances"). \
            set_font_scale(1). \
            set_save_fig_size("a3"). \
            plot()
