from me_main_libs import *

from bokeh.palettes import Dark2_5, Category20c, brewer
from bokeh.transform import cumsum
from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.palettes import brewer
from bokeh.models import HoverTool, DatetimeTickFormatter, NumeralTickFormatter

import itertools
from math import pi


def _create_colors():
    colors = itertools.cycle(Category20c)
    return colors


def plot_bar_basic(df, x_name, y_name, title, plot_height=350, plot_width=None,
                   output_file_=None):
    '''
    output_file:'*.html'
    '''
    if output_file_:
        output_file(output_file_)

    p = figure(x_range=df[x_name],
               plot_height=plot_height,
               plot_width=plot_width,
               title=title,
               toolbar_location=None,
               tools="hover",
               tooltips=f"@{x_name}: @{y_name}",
               )

    p.vbar(x=x_name, top=y_name, width=0.9, source=df)
    p.xgrid.grid_line_color = None

    if plot_width:
        p.plot_width = plot_width
    else:
        p.sizing_mode = "stretch_width"
    return p


def plot_bar_stacked(df, x_name, y_names, title, y_range_start=0, y_range_end=None,
                     plot_height=350, plot_width=None,
                     output_file_=None):
    '''
    only works if len(y_names)>=3

    output_file:'*.html'
    '''

    if output_file_:
        output_file(output_file_)

    tooltips = []
    tooltips.append((f'{x_name}', f'@{x_name}'))
    for y_name in y_names:
        tooltips.append((f'{y_name}', f'@{y_name}'))

    p = figure(x_range=df[x_name], plot_height=plot_height,
               plot_width=plot_width,
               title=title,
               toolbar_location=None,
               tools="hover",
               tooltips=tooltips,
               )

    p.vbar_stack(y_names, x=x_name, width=0.9, color=brewer['Spectral'][len(y_names)],
                 source=df,
                 legend_label=y_names)

    p.x_range.range_padding = 0.05
    p.axis.minor_tick_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_left"

    p.xgrid.grid_line_color = None
    p.y_range.start = y_range_start
    if y_range_end:
        p.y_range.end = y_range_end

    if plot_width:
        p.plot_width = plot_width
    else:
        p.sizing_mode = "stretch_width"
    return p


def plot_histogram(series, title, draw_curves=False,
                   plot_height=350, plot_width=None,
                   output_file_=None):

    if output_file_:
        output_file(output_file_)

    series = series.values.reshape(1, -1)[0]
    bins = 50
    hist, edges = np.histogram(series, density=True, bins=bins)

    p = figure(title=title, plot_height=plot_height, plot_width=plot_width,
               toolbar_location=None,
               )

    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)

    if draw_curves:
        mu = series.mean()
        sigma = series.std()
        x = np.linspace(min(series), max(series), 100)
        pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
        # cdf = ((1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2)*100
        p.line(x, pdf, line_color="#ff8888", line_width=4,
               alpha=0.7, legend_label="PDF")
        # p.line(x, cdf, line_color="orange", line_width=2,
        #        alpha=0.7, legend_label="CDF")

        p.legend.location = "center_right"

    p.yaxis.axis_label = 'Prob(x)'
    if plot_width:
        p.plot_width = plot_width
    else:
        p.sizing_mode = "stretch_width"
    return p


def plot_candlestick(ohlc, title, plot_height=350, plot_width=None,
                     output_file_=None):
    '''
    https://docs.bokeh.org/en/latest/docs/gallery/candlestick.html
    '''
    if output_file_:
        output_file(output_file_)

    ohlc.index.name = 'date'
    ohlc.reset_index(inplace=True)

    inc = ohlc.close > ohlc.open
    dec = ohlc.open > ohlc.close
    w = 12*60*60*1000  # half day in ms

    tools = "crosshair,box_zoom,reset,save"

    p = figure(title=title, plot_height=plot_height, plot_width=plot_width,
               toolbar_location='right',
               tools=tools,
               x_axis_type="datetime"
               )
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha = 0.3

    p1 = p.segment('date', 'high', 'date', 'low', color="black", source=ohlc)
    p.vbar(ohlc.date[inc], w, ohlc.open[inc], ohlc.close[inc],
           fill_color="#D5E1DD", line_color="black")
    p.vbar(ohlc.date[dec], w, ohlc.open[dec], ohlc.close[dec],
           fill_color="#F2583E", line_color="black")

    tooltips = []
    tooltips.append(('date', '@date{%F}'))
    for y_name in ['open', 'high', 'low', 'close']:
        tooltips.append((f'{y_name}', f'@{y_name}'))

    p.add_tools(HoverTool(tooltips=tooltips,
                          formatters={'@date': 'datetime'},
                          renderers=[p1],
                          mode='vline'))
    p.yaxis.formatter = NumeralTickFormatter(format="$0.00")
    p.xaxis.formatter = DatetimeTickFormatter(months="%m-%d")

    p.x_range.range_padding = 0.02
    p.toolbar.autohide = True
    p.toolbar.logo = None
    if plot_width:
        p.plot_width = plot_width
    else:
        p.sizing_mode = "stretch_width"
    return p


def plot_line(series, title, x_axis_type='datetime', plot_height=350, plot_width=None, output_file_=None):
    '''
    x_axis_type: 'linear', 'log', 'datetime', 'mercator'
    output_file:'*.html'
    '''

    if output_file_:
        output_file(output_file_)

    tools = "crosshair,box_zoom,reset,save"
    p = figure(title=title, plot_height=plot_height, plot_width=plot_width,
               toolbar_location='right',
               tools=tools,
               x_axis_type=x_axis_type)

    p.line(series.index, series.squeeze())

    p.x_range.range_padding = 0
    p.toolbar.autohide = True
    p.toolbar.logo = None
    if plot_width:
        p.plot_width = plot_width
    else:
        p.sizing_mode = "stretch_width"
    return p


def plot_multi_line(df, title, x_axis_type='datetime', plot_height=350, plot_width=None,
                    legend_orientation="horizontal",
                    legend_location="top_left",
                    output_file_=None):
    '''
    x_axis_type: 'linear', 'log', 'datetime', 'mercator'
    '''

    if output_file_:
        output_file(output_file_)

    tools = "crosshair,box_zoom,reset,save"
    p = figure(title=title, plot_height=plot_height, plot_width=plot_width,
               toolbar_location='right', tools=tools,
               x_axis_type=x_axis_type)

    colors = itertools.cycle(Dark2_5)
    for col, color in zip(df.columns, colors):
        p.line(df.index, df[col], color=color, legend_label=col)

    p.legend.location = legend_location
    p.legend.orientation = legend_orientation
    p.legend.click_policy = "hide"

    p.x_range.range_padding = 0
    p.toolbar.autohide = True
    p.toolbar.logo = None
    if plot_width:
        p.plot_width = plot_width
    else:
        p.sizing_mode = "stretch_width"
    return p


def plot_pie_chart(df, x_name, y_name, title, plot_height=350, plot_width=500,
                   output_file_=None):

    if output_file_:
        output_file(output_file_)

    df['angle'] = df[y_name]/df[y_name].sum() * 2*pi
    df['color'] = Category20c[len(df)]

    p = figure(plot_height=plot_height,
               plot_width=plot_width,
               title=title,
               toolbar_location=None,
               tools="hover",
               tooltips=f"@{x_name}: @{y_name}",
               x_range=(-0.5, 1.0)
               )

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field=x_name, source=df)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    return p


def plot_stacked_area(df, title, x_axis_type='linear', y_range_start=0,
                      y_range_end=None, plot_height=350, plot_width=None,
                      output_file_=None):
    '''
    hover tooltips have not been implemented for them yet 
    x_axis_type: 'linear', 'log', 'datetime', 'mercator'
    output_file:'*.html'
    '''

    if output_file_:
        output_file(output_file_)

    p = figure(plot_height=plot_height,
               plot_width=plot_width,
               title=title,
               toolbar_location=None,
               tools='crosshair',
               x_range=(0, len(df)-1),
               x_axis_type=x_axis_type)

    df.index.name = 'index'
    N = len(df.columns)
    p1 = p.varea_stack(stackers=list(df.columns), x='index',
                       color=brewer['Spectral'][N],
                       legend_label=list(df.columns), source=df)

    p.axis.minor_tick_line_color = None
    p.legend.orientation = 'horizontal'
    p.legend.location = 'top_left'
    p.legend.click_policy = "hide"

    p.y_range.start = 0
    if y_range_end:
        p.y_range.end = y_range_end
    if plot_width:
        p.plot_width = plot_width
    else:
        p.sizing_mode = "stretch_width"
    return p
