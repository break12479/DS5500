# import pandas as pd
# import glob


# file_list = glob.glob("./data/matches/matches_*.csv")
# dfs = []

# # Loop through each file and read it into a DataFrame
# for file in file_list:
#     df = pd.read_csv(file)
#     dfs.append(df)

# # Concatenate all DataFrames into a single DataFrame
# combined_df = pd.concat(dfs, ignore_index=True)
# combined_df.to_csv('./data/matches.csv', index=False)

# # Display the first few rows of the combined DataFrame
# print(combined_df.head())
import pandas as pd
import glob


file_list = glob.glob("./data/timeline/matchesWithTimeLine_*.csv")
dfs = []

# Loop through each file and read it into a DataFrame
for file in file_list:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv('./data/timeline.csv', index=False)

# Display the first few rows of the combined DataFrame
print(combined_df.head())