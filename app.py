from flask import Flask, render_template, request, redirect
from data import data_load
from model import scale_col_by_col, scale_col_by_row
from sklearn.neighbors import NearestNeighbors


app = Flask(__name__)

sql_queery = 'SELECT * FROM beer_data'
data = data_load(sql_queery)
beer_style = data['beername'].unique()



@app.route('/')
def home():
    return render_template('main.html', style=beer_style)


@app.route('/result', methods=['GET', 'POST'])
def result():
    # get, post
    select = request.args.get('style_select')
    if select:
        select = select
    else:
        return redirect('/')
    
    data = data_load(sql_queery)
    
    
    tasting_profile_cols = ['astringency', 'body', 'alcohol', 'bitter', 'sweet', 'sour', 'salty', 'fruits', 'hoppy', 'spices', 'malty']
    chem_cols = ['abv', 'minibu', 'maxibu']
        
        
    # Scale values in tasting profile features (across rows)
    data = scale_col_by_row(data, tasting_profile_cols)

    # Scale values in tasting profile features (across columns)
    data = scale_col_by_col(data, tasting_profile_cols)

    # Scale values in chemical features (across columns)
    data = scale_col_by_col(data, chem_cols)

    df = data.drop(['name', 'description', 'review_aroma', 'review_appearance', 'review_palate', 'review_taste', 'review_overall', 'number_of_reviews'],axis=1)

    # Use only numeric features
    df_num = df.select_dtypes(exclude=['object'])

    # user_input = select # user가 입력한 값

    test_data = data[data['beername'] == str(select)]
    num_input = df_num.loc[test_data.index].values

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


    # Detect beer style
    style_input = test_data['style'].iloc[0]
    top_5_same_style_rec = get_neighbors(data, num_input, style_input, same_style=True)
    top_5_false_style_rec = get_neighbors(data, num_input, style_input, same_style=False)
        
    return render_template('result.html', select_style=select, tables=[top_5_same_style_rec.to_html(classes='data')], titles=[''], \
                            tabless=[top_5_false_style_rec.to_html(classes='data')], titless=[''])  
    

if __name__ == '__main__':
    app.run()