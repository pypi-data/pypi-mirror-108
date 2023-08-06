# DottedDict
 
## Examples
```python
from nestydict import Nesty

normal_dict = {
    "metrics.cost.name": "cost_micros",
    "metrics.cost.value": 123123,
    "metrics.campaign": {"name": "Extra Clicks", "metrics.cost_micros": 100},
}

dotted = Nesty.from_dict(normal_dict)

dotted
# {
#     "metrics": {
#         "cost": {
#             "name": "cost_micros",
#             "value": 123123
#         },
#         "campaign": {
#             "name": "Extra Clicks",
#             "metrics": {
#                 "cost_micros": 100
#             }
#         }
#     }
# }
```

```python
from nestydict import Nesty

dotted = Nesty()
dotted["metrics.cost.name"] = "cost_micros"
dotted["metrics.cost.id"] = 123123
dotted["metrics.cost.type"] = "money"
dotted["metrics.campaign"] = [{"A": 1}]

dotted
# {
#     "metrics": {
#         "cost": {
#           "name": "cost_micros",
#           "id": 123123,
#           "type": "money"
#       },
#         "campaign": [{"A": 1}],
#     }
# }

dotted["metrics.cost"]
# {
#     "name": "cost_micros",
#     "id": 123123,
#     "type": "money"
# }
```
