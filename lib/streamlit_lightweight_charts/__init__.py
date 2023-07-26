import os
from typing import Dict, List
from enum import Enum
import streamlit.components.v1 as components

_COMPONENT_NAME = "streamlit_lightweight_charts"
_RELEASE = True

class Chart(str, Enum):
    Area = 'addAreaSeries'
    Baseline = 'addBaselineSeries'
    Histogram = 'addHistogramSeries'
    Line = 'addLineSeries'
    Bar = 'addBarSeries'
    Candlestick = 'addCandlestickSeries'

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend","build")

if not _RELEASE:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        # path=build_dir,
        url="http://localhost:3001",
    )
else:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        path=build_dir
    )

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def renderLightweightCharts(charts: List, key: str = None):
    """Create a new instance of "renderLightweightCharts".

    Parameters
    ----------
    charts: <List of Dicts>

        chart: <Dict>
        https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions

        series: <List of Dicts>
            https://tradingview.github.io/lightweight-charts/docs/series-types

            type: <str-enum>
                Area
                Bar
                Baseline
                Candlestick
                Histogram
                Line

            data: <List of Dicts> accordingly to series type

            options: <Dict> with style options

            priceScale: <Dict> optional
    
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    """

    return _component_func(
        charts=charts,
        key=key
    )