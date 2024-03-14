from resp.apis.serp_api import Serp
from resp.apis.cnnp import connected_papers
from resp.apis.semantic_s import Semantic_Scholar
from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.arxiv_api import Arxiv
from resp.resp import Resp

ac           = ACM()
acm_result   = ac.acm('Machine Learning', max_pages = 1)
print(acm_result)