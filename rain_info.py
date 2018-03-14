import pandas as pd

pd.options.display.encoding = str('utf-8')

df1 = pd.read_csv("total/rain_station_981.csv", encoding='utf-8')
df2 = pd.read_csv("total/rain_station_213.csv", encoding='utf-8')
df3 = pd.read_csv("total/rain_station_2017_5.csv", encoding='utf-8')

merge_df = pd.concat([df1, df2, df3], axis=0)
merge_df["date"] = pd.to_datetime(merge_df.date)
merge_df.sort_values(by='date')
merge_df.set_index("date", inplace=True)
merge_df.sort_index(inplace=True)
#print(merge_df)
merge_df.to_csv('total/rain_info.csv', encoding='utf-8')
