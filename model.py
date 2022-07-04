import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from data import data_load


sql_queery = 'SELECT * FROM beer_data'
data = data_load(sql_queery)
    
    
tasting_profile_cols = ['astringency', 'body', 'alcohol', 'bitter', 'sweet', 'sour', 'salty', 'fruits', 'hoppy', 'spices', 'malty']
chem_cols = ['abv', 'minibu', 'maxibu']
        

def scale_col_by_row(df, cols):
    scaler = MinMaxScaler()
    # Scale values by row
    scaled_cols = pd.DataFrame(scaler.fit_transform(df[cols].T).T, columns=cols)
    df[cols] = scaled_cols
    return df

def scale_col_by_col(df, cols):
    scaler = MinMaxScaler()
    # Scale values by column
    scaled_cols = pd.DataFrame(scaler.fit_transform(df[cols]), columns=cols)
    df[cols] = scaled_cols
    return df


# Scale values in tasting profile features (across rows)
data = scale_col_by_row(data, tasting_profile_cols)

# Scale values in tasting profile features (across columns)
data = scale_col_by_col(data, tasting_profile_cols)

# Scale values in chemical features (across columns)
data = scale_col_by_col(data, chem_cols)

df = data.drop(['name', 'description', 'review_aroma', 'review_appearance', 'review_palate', 'review_taste', 'review_overall', 'number_of_reviews'],axis=1)

# Use only numeric features
df_num = df.select_dtypes(exclude=['object'])



user_input = df['beername'].sample().iloc[0]

test_data = data[data['beername'] == user_input]
num_input = df_num.loc[test_data.index].values

style_input = test_data['style'].iloc[0]
    

def get_neighbors(data, num_input, style_input, same_style=False):
    if same_style==True:
        # Locate beers of same style
        df_target = data[data["style"] == style_input].reset_index(drop=True)
    else:
        # Locate beers of different styles
        df_target = data[data["style"] != style_input].reset_index(drop=True)

    df_target_num = df_num.loc[df_target.index]
    # Calculate similarities (n_neighbors=6 for 5 recommendations)
    search = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(df_target_num)
    _ , queried_indices = search.kneighbors(num_input)
    # Top 5 recommendations
    target_rec_df = df_target.loc[queried_indices[0][1:]]
    target_rec_df = target_rec_df.sort_values(by=['review_overall'], ascending=False)
    target_rec_df = target_rec_df[['name', 'brewery', 'style', 'review_overall']]
    target_rec_df.index = range(1, 6)
    target_rec_df.drop('review_overall', axis=1, inplace=True)
    return target_rec_df


top_5_same_style_rec = get_neighbors(data, num_input, style_input, same_style=True)


for list in top_5_same_style_rec:
    print(list)

    