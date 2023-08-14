from utils import get_data, read_data
import pdb
read_data('data/附件2 慢性病及相关因素流调数据.xlsx')
data = get_data()
pdb.set_trace()
data.statistics("food_diversity")

pdb.set_trace()