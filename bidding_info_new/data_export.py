import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:87886922@localhost:3306/bidding_info')

info_detail = pd.read_sql_table('info_detail', engine)

combine_data = pd.DataFrame()

i = 0

for title in info_detail['bidding_table_titles_list']:
    sub_title = title.split('|')
    print(sub_title)
    i = i + 1
    # sub_item = info_detail['bidding_table_items_list'][i].split(',')

    # print(len(sub_item))
    # print(len(sub_title))

    # single_data = pd.DataFrame(np.array(sub_item),columns=sub_title)
    # print(single_data)


    # print(title.split(','))
# for item in info_detail['bidding_table_items_list']:
#     print(item.split(','))
        # single_data = pd.DataFrame(data=item,columns=title)
        # print(single_data)
