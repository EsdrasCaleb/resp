from resp.apis.serp_api import Serp
from resp.apis.cnnp import connected_papers
from resp.apis.semantic_s import Semantic_Scholar
from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.scholar_api import Scholar
from resp.apis.arxiv_api import Arxiv
from resp.resp import Resp
import random

topics = ["Software Engineering","Machine Learning","software architecture"]
sc = Scholar()
result = sc.query(topics[ random.randint(0, len(topics)-1)],1)
print(result)