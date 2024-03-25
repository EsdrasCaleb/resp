from resp.apis.serp_api import Serp
from resp.apis.cnnp import connected_papers
from resp.apis.semantic_s import Semantic_Scholar
from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.scholar_api import Scholar
from resp.apis.arxiv_api import Arxiv
from resp.apis.trends_api import Trends
from resp.resp import Resp
import random

#datas de 2004 a 2023

#topics = ["Software Engineering","Machine Learning","software architecture"]
#sc = Scholar()
#result = sc.query(topics[ random.randint(0, len(topics)-1)],1)
#td = Trends()
#result = td.query("serious game")

acm = ACM()
print(acm.all_paper(0,1,10))
#acm.query(topics[ random.randint(0, len(topics)-1)],1)