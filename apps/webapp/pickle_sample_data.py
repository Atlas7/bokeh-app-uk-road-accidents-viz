"""
Purpose:
- Turn the input CSV into a Pandas Dataframe, pickle and store onto disk.
- (may be handy) Create bounding boxes (`bboxes`), pickle and store onto disk

Prerequisite: already have the appropriate CSV file in the data directory.

Run this script at the repository root: python process_sample_data.py
"""
import pandas as pd
import pickle
from utils import add_webm_xys

df = pd.read_csv('./data/dftRoadSafety_Accidents_2016.csv', usecols=["Accident_Index", "Longitude", "Latitude"])
df=df.dropna()
df = add_webm_xys(df)
df.to_pickle("./data/dftRoadSafety_Accidents_2016_tiny.pkl")
usecols = ["Accident_Index", "Longitude", "Latitude", "webm_x", "webm_y"]
df2 = pd.read_pickle('./data/dftRoadSafety_Accidents_2016_tiny.pkl')[usecols]
bboxes = {
  "gb": ((-15.381, 7.251), (48.749, 61.502)),
  "gb_mainland": ( (-12.129, 5.120), (49.710, 58.745)),
  "gb_long": ((-8.745, 2.241), (48.749, 61.502)),
  "gb_wide": ((-21.709, 15.293), (48.749, 61.502)),
  "london": ((-0.643, 0.434), (51.200, 51.761)),
  "london_2": ((-0.1696, 0.0130), (51.4546, 51.5519)),
  "london_3": ((-0.1330, -0.0235), (51.4741, 51.5322)),  
  "manchester": ((-3.049, -1.505), (52.975, 53.865))
}
with open('./data/bboxes.pkl', 'wb') as handle:
    pickle.dump(bboxes, handle, protocol=pickle.HIGHEST_PROTOCOL)