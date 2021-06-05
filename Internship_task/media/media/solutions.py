'''
1. SQL query to find out details of users who have visited ‘pricing’ + 1 other page, and have a session time > 45 seconds.
'''
'''
select * from events 
where (LENGTH(page_visited) - LENGTH(REPLACE(page_visited,',','')) + 1)=2 
and 
find_in_set('pricing', page_visited) 
and
timestampdiff(second,session_start,session_end)>45;

'''

''' 
2. Create a function that counts the number of rows where value=1 on a per day basis, for each column. 
'''

user = pd.read_csv('E:\\user_data.csv')
session = pd.read_csv('E:\\session_data.csv')
output = pd.merge(user,session,on='session_id',how='outer')[['session_id','event_date','is_rp','signup_start','signup_complete','active_after_7d']]
dates = (pd.read_csv("E:\\user_data.csv", usecols=["event_date"]))
dates_list= dates['event_date'].tolist()
date_set=list(set(dates_list))
count=[]
output_list= output.to_numpy().tolist()
for date in date_set:
    c=0
    for row in output_list:
            
        if row[1]==date and int(row[2])==1 and int(row[3])==1 and int(row[4])==1 and int(row[5])==1:
            c+=1

    count.append([date,c])
print("\nCreate a function that counts the number of rows where value=1 on a per day basis, for each column.\n\n")
print(*count, sep='\n')

''' Q.3 '''

import pandas as pd
col_list = ["is_rp", "signup_start", "signup_complete", "active_after_7d"]
df = pd.read_csv("E:\\session_sum.csv")
ratio_list=['']
for i in range(1, len(col_list)):
    ratio=int(df[col_list[i]])/int(df[col_list[i-1]])
    ratio_list.append(ratio)

new_data = pd.DataFrame([ratio_list], columns=col_list)
new_data.to_csv("E:\\session_sum_ratio.csv", index=False)
ratio_data = pd.read_csv("E:\\session_sum_ratio.csv")
print('\n',ratio_data)

''' Plot the graph '''

import matplotlib.pyplot as plt
dates = (pd.read_csv("E:\\user_data.csv", usecols=["event_date"]))
dates_list= dates['event_date'].tolist()
date_set=list(set(dates_list))
visitors=[]
print("\n Number of visitors per day\n")
for date in date_set:
    x=dates_list.count(date)
    visitors.append(x)
    print(date, x)
plt.plot(date_set, visitors)
plt.title('Number of visitors per day')
plt.show()


''' Q. 4 '''

import pandas as pd
import numpy as np
df5 = pd.read_csv('E://event_data.csv')
x = df5['payload_column'].str.split('&').explode('payload_column')
x = pd.DataFrame(x)

x['evnt_ts']=np.repeat('23:00',63)
x['visitor_id']=np.repeat('123',63)

x[['payload_key','payload_val']] = x['payload_column'].str.split('=',n=1, expand=True)

print(x)