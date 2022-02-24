import json
import base64

import dash
from dash import html, dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Overall TODO:
# - add and remove nodes
# - flexible "data card" displays node properties when selected

# https://dash.plotly.com/cytoscape
app = dash.Dash(__name__)

graphData = {
    'nodes': [
        {'data': {'id': 'one', 'label': 'Node 1'}},
        {'data': {'id': 'two', 'label': 'Node 2', 'img': 'https://placekitten.com/100/100'}},
        {'data': {'id': 'three', 'label': 'Node 3'}, 'classes': 'person'},
    ],
    'edges': [
        {'data': {'source': 'one', 'target': 'two'}},
        {'data': {'source': 'one', 'target': 'three'}},
    ]
}

styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        },
        'img': {}
    }

stylesheet = [
        # groups
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)'
            }
        },
        # classes
        {
            'selector': '.person',
            'style': {
                'shape': 'triangle'
            }
        }
    ]

app.layout = html.Div([
    dcc.Store(id='graph-data',
        storage_type='local',
        data = graphData
    ),
    cyto.Cytoscape(
        id='main-graph',
        layout={'name': 'cose', 'animate': True, 'fit': True, 'padding': 60},
        style={'width': '100%', 'height': '600px', 'outline': 'solid black'},
        responsive=True,
        stylesheet=stylesheet,
        elements={}
    ),
    html.Div(id='data-card', children=[
        html.Img(id='tap-node-image', style=styles['img']),
        html.Pre(
            id='tap-node-data',
            style=styles['pre'],
            contentEditable="true", # idk why this has to be a string
            hidden=True
            ),
        ]
    ),
    html.Hr(),
    html.Div(id='upload-download', children=[
        dcc.Upload(
            id='upload-graph',
            children=html.Button('Upload Graph'),
            accept='application/json'
        ),
        html.Button('Download Graph', id='btn-download-graph'),
        dcc.Download(id='download-graph'),
        ]
    ),
    html.Hr()
])

###### Graph Upload/Download and Storage ######
@app.callback(Output('download-graph', 'data'),
              Input('btn-download-graph', 'n_clicks'),
              State('graph-data', 'data'),
              prevent_initial_call=True)
def downloadGraph(n_clicks, data):
    return dict(
            content=json.dumps(data),
            filename='graph.json',
            type='application/json'
        )

@app.callback(Output('graph-data', 'data'),
              Input('upload-graph', 'contents'),
              State('graph-data', 'data'))
def uploadGraph(contents, data):
    # nothing actually uploaded
    if contents is None or contents == '':
        raise PreventUpdate
    # data comes in as something like:
    # data:application/json;base64,longstringofbase64data
    try:
        data = contents.split(';')[1]
        data = data.split(',')[1]
        data = base64.b64decode(data)
        data = data.decode()
    except:
        raise ValueError('uploaded file was bogus')

    # something was uploaded, store it and render
    data = json.loads(data)
    print('storing new graph data')
    return data

###### Node Selection/Data Rendering ######

# render the graph on a change in store
@app.callback(Output('main-graph', 'elements'),
              Input('graph-data', 'modified_timestamp'),
              State('graph-data', 'data'))
def renderGraph(ts, data):
    print('rendering')
    return data

# TODO update the store if the graph is edited (circular callback)
# https://dash.plotly.com/advanced-callbacks#circular-callbacks

# display selected node's raw JSON as text
@app.callback(Output('tap-node-data', 'children'),
              Output('tap-node-data', 'hidden'),
              Input('main-graph', 'selectedNodeData'))
def displaySelectedNodeData(data):
    if data is None or data == []:
        return ('Nothing selected', True)
    return (json.dumps(data, indent=2), False)
# TODO make editable content sync with data

# display selected node's 'img' attr
# @app.callback(Output('tap-node-image', 'src'),
#               Input('main-graph', 'selectedNodeData'))
# def displaySelectedNodeImage(data):
#     if data is None:
#         return None
#     elif 'img' not in data or data['img'] is None:
#         return None
#     else:
#         return data['img']

if __name__ == '__main__':
    app.run_server(debug=True)
