# Capt'n AI for Nanobit
> Marketing campaigns optimization


## Install

`pip install captn-nanobit-client`

## How to use 


```python
from captn_nanobit_client.api import authorize, predict
from captn_nanobit_client.testing import get_test_dataframe
from captn_nanobit_client.plotly_graph import plot_prediction
# server is one of "staging" or "production"
server = "staging"

token = authorize(username=username, password=password, server=server)
```

Get pandas dataframe

```python
df = get_test_dataframe()
```

Run the code below to make a prediction

```python
prediction = predict(df, token=token)
```

Run the code below to draw a graph

```python
graph = plot_prediction(df, prediction, last_n_days=3, target_day=29)
# uncomment this line to show the graph
# graph.show()
```

<img src="https://nanobit.api.captn.ai/images/captn_graph.png?v2021.06.07" width="781" style="max-width: 781px">
