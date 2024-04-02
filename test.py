from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.scholar_api import Scholar
from resp.apis.trends_api import Trends
from pytrends.request import TrendReq
import random
import csv
import json
#"Computing methodologies","Computer graphics","Machine learning","Power and energy","Hardware"

pytrends = TrendReq(hl='pt-Br', tz=360, timeout=(10, 25), retries=0, backoff_factor=0,proxies=[])
pytrends.build_payload(kw_list=["Computing methodologies",], timeframe=['2004-01-01 2021-12-31'])
result =  pytrends.interest_over_time()
print(result)
print(json.dumps(result))

