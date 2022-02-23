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
        }
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
                {'data': {'id': 'two', 'label': 'Node 2'}},
                {'data': {'id': 'three', 'label': 'Node 3'}, 'classes': 'person'},
            ],
            'edges': [
                {'data': {'source': 'one', 'target': 'two'}},
                {'data': {'source': 'one', 'target': 'three'}},
            ]
        }
    ),
    html.Pre(id='tap-node-data', style=styles['pre'])
])

@app.callback(Output('tap-node-data', 'children'),
              Input('main-graph', 'selectedNodeData'))
def displaySelectedNodeData(data):
    if data is None or len(data) is 0:
        return 'Nothing selected'
    return json.dumps(data, indent=2)

if __name__ == '__main__':
    app.run_server(debug=True)
