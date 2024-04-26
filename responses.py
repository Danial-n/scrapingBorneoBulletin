import pandas as pd
from datetime import date

today = date.today()
news_file = pd.read_csv(f'todaynews_2024-04-24.csv')

# Sort news by category
def sort_news(category: str) -> str:
    filtered_news = news_file[news_file['Category'] == category]
    response = []
    for _, row in filtered_news.iterrows():
        news_item = f"[{row['Category'].upper()}] \n[{row['Headline']}]({row['Link']}) \n({row['Date']})"
        response.append(news_item)
    return response

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return ['Umm...']
        
    elif 'hello' in lowered:
        return ['Hello there']
    
    elif 'get news' in lowered:
        return ['Collecting news...']

    elif lowered in [str(i) for i in range(1, 11)]:
        category_list = {
            '1': 'national',
            '2': 'southeast',
            '3': 'world',
            '4': 'business',
            '5': 'tech',
            '6': 'lifestyle',
            '7': 'entertainment',
            '8': 'features',
            '9': 'sports',
            '10': 'opinion'
        }
        response = sort_news(category_list[lowered])
        return response

    elif 'all' in lowered:
        response = []
        for _, row in news_file.iterrows():
            news_item = f"[{row['Category'].upper()}] \n[{row['Headline']}]({row['Link']}) \n({row['Date']})"
            response.append(news_item)
        return response
        
    
    
    elif 'read article' in lowered:
        return ['article description - TBA']



    else:
        return ['Huh']