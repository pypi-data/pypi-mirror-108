# ECMind blue client: Workflow

Helper modules for the `ecmind_blue_client` to ease the work with workflows, models and organisations. See discussion here: https://hub.ecmind.ch/t/119

## Installation

`pip install ecmind_blue_client_workflow`


## Usage

```python
from ecmind_blue_client.tcp_client import TcpClient as Client
from ecmind_blue_client_workflow import workflow

client = Client(hostname='localhost', port=4000, appname='test', username='root', password='optimal')
print(workflow.get_organisations(client, only_active=True))
```