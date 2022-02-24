import json

import dash
from dash import html, dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output

# https://dash.plotly.com/cytoscape
app = dash.Dash(__name__)

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
    cyto.Cytoscape(
        id='main-graph',
        layout={'name': 'cose', 'animate': True, 'fit': True, 'padding': 60},
        style={'width': '100%', 'height': '600px', 'outline': 'solid black'},
        responsive=True,
        stylesheet=stylesheet,
        elements={
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
    ),
    html.Img(id='tap-node-image', style=styles['img']),
    html.Pre(id='tap-node-data', style=styles['pre'])
])

@app.callback(Output('tap-node-data', 'children'),
              Input('main-graph', 'tapNodeData'))
def displaySelectedNodeData(data):
    if data is None:
        return 'Nothing selected'
    return json.dumps(data, indent=2)

@app.callback(Output('tap-node-image', 'src'),
              Input('main-graph', 'tapNodeData'))
def displaySelectedNodeImage(data):
    if data is None:
        return None
    elif 'img' not in data or data['img'] is None:
        return None
    else:
        return data['img']

if __name__ == '__main__':
    app.run_server(debug=True)
