import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:87886922@localhost:3306/bidding_info')

info_detail = pd.read_sql_table('info_detail', engine)

combine_data = pd.DataFrame()

i = 0
for index , row in info_detail.iterrows():
    # print(index)
    sub_title = row[1].split('|')
    item = row[2].split('|')


    i = 0
    pop_list = []
    while i < len(sub_title):
        # print(sub_title[i])
        if sub_title[i] == '':
            print("x")
            pop_list.append(i)
        i += 1

    if len(pop_list) > 0 or len(sub_title) != len(item):
        continue;


    new_dict = dict(zip(sub_title,item))
    new_pd = pd.DataFrame(data=new_dict, index=[0], columns=sub_title)


    # new_pd = new_pd.drop('',axis=1)
    print(index)
    # print(new_pd)
    if index == 0 :
        combine_data = new_pd
    else:
        # combine_data = combine_data.reset_index()
        # new_pd = new_pd.reset_index()
        try:
            combine_data = pd.concat([combine_data, new_pd] , axis=0, ignore_index=True)
        except:
            print("出错了")
    print(combine_data)
    

combine_data.to_excel('final_format.xlsx', encoding='utf8')




# for title in info_detail['bidding_table_titles_list']:
#     sub_title = title.split('|')
#     print(sub_title)
#     i = i + 1
    # sub_item = info_detail['bidding_table_items_list'][i].split(',')

    # print(len(sub_item))
    # print(len(sub_title))

    # single_data = pd.DataFrame(np.array(sub_item),columns=sub_title)
    # print(single_data)


    # print(title.split(','))
# for item in info_detail['bidding_table_items_list']:
#     single_data = pd.DataFrame(np.array(item.split('|')))
#     print(single_data)
    # print(item.split('|'))
    # print(single_data)
