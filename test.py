from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.scholar_api import Scholar
from resp.apis.trends_api import Trends
import random
import csv
sc = Scholar()
result = sc.paper_citations("Center-based 3D Object Detection and Tracking", 2021)
print(result)

