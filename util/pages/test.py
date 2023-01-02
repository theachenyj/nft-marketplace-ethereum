import requests
import pandas as pd
import json
import util.constants.urls as urls

api_data = requests.get(url=urls.url_sales_change, headers={})
json_data = json.loads(api_data.text)
save_dict = {"Month": [], "Change": []}
for item in json_data:
    if(item["PLATFORM_NAME"] == 'looksrare' and item["BLOCK_MONTH"]  >= '2022-02-01'):
        save_dict["Month"].append(item["BLOCK_MONTH"])
        save_dict["Change"].append(item["SALES_COUNT_MOM"])
df = pd.DataFrame(data=save_dict,columns=['Month', 'Change'])
df.sort_values("Month", inplace=True)
print(df)