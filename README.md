# linkinator

It uh... links things.

The concept here is that *building* graphs (e.g. as part of data ingestion) is  hard. Tools like Gephi exist to analyze the data, but they rely mostly on having the data already available as nice clean CSV files or similar. Trying to actually *create* those CSV files is the problem.

Currently, this doesn't do much. You can run it using:

```
pipenv install
pipenv shell
python run.py
```

This will (should) print a localhost URL and port that you can visit to see the graph. It comes pre-loaded with a few nodes and an edge to mess with, and if you click on a node the raw data for that node will be loaded into the page.

You can upload and download graphs in a weird JSON structure, which is just a test for being able to do that at all. In the future, it'll be a nice, useful format (NetworkX should hopefully enable this fairly easily).

The next steps are to make it fairly easy to click somewhere on the page, select "new node" from a menu, and then enter data into the new node. Similar with edges.
