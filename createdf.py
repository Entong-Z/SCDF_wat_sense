import pandas as pd
from datetime import datetime

#df = pd.DataFrame(columns = ["phone_num",
#                             "text",
#                             "keywords",
#                             "time",
#                             "predicted_event_ID",
#                             "action"])

df = pd.DataFrame(columns = ["Time", "Keywords", "Type", "Event ID"])

print(df)
df.to_pickle("df.pkl")