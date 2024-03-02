import numpy as np
from dash import Dash, html, dcc, callback, Output, Input,State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Dash(__name__)

grid = np.zeros((400,400))
hidden_grid = np.zeros((400,400))
fig  = go.Figure(px.imshow(grid,color_continuous_scale="gray",zmin=0, zmax=1))
fig.add_trace(go.Scatter(x=[],y=[],mode='markers',))
fig.update_layout(width=400,
        height=400,
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        plot_bgcolor="white",
        clickmode="event",
        )
fig.update_traces(hoverinfo="none", hovertemplate=None)

fig2 = go.Figure(px.imshow(grid,color_continuous_scale="gray"))
fig.update_layout(width=400,
        height=400,
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        plot_bgcolor="white",
        clickmode="event",
        )
fig.update_traces(hoverinfo="none", hovertemplate=None)

app.layout = html.Div([dcc.Graph(id="ant-pos-plot",figure=fig,config={"displayModeBar": False},),
    dcc.Graph(id="fft-plot",figure=fig2,config={"displayModeBar": False},),
    html.Div(id="click-data")])


@app.callback(Output("click-data","children"),
        Output("ant-pos-plot","figure"),
        Output("fft-plot","figure"),
        Input("ant-pos-plot","clickData"),
        State("ant-pos-plot","figure"),
        State("fft-plot","figure"))
def display_click_data(clickData,_fig,_fig2):
    current_x = _fig['data'][1]['x']
    current_y = _fig['data'][1]['y']
    
    if clickData:
        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']
        print(x,y)

        if clickData['points'][0]['curveNumber'] == 0:
            current_x.append(x)
            current_y.append(y)
        else:
            current_x.remove(x)
            current_y.remove(y)
        _fig['data'][1].update(x=current_x,y=current_y)
    hidden_grid[:,:]=0
    hidden_grid[current_x,current_y] = 1
    fourier_tr = np.abs(np.fft.fftshift(np.fft.fft2(hidden_grid)))
    _fig2['data'][0]['z'] = fourier_tr
    return str(clickData),_fig,_fig2

if __name__ == '__main__':
    app.run_server(debug=True)

