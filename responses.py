import pandas as pd
from datetime import date

today = date.today()

def get_file():
    try:
        return pd.read_csv(f'todaynews_{today}.csv') 
    except FileNotFoundError:
        return pd.DataFrame()

# Sort news by category
def sort_news(category: str) -> str:
    news_file = get_file()
    filtered_news = news_file[news_file['Category'] == category]
    response = []
    if filtered_news.empty:
        response = [f'No news in {category} today']
    else:
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
    
    elif 'about' in lowered:
        comm_list = """
- **!update**: To update today news
- **!news**: To call main menu for news
- **!1 (available up to 10)**: Shortcut to get news
- **!all**: To get all news
    """
        return ['I am a bot that provide you today news from Borneo Bulletin. \nAvailable command: \n', comm_list]

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
        news_file = get_file()
        if news_file.empty:
            response ['News Not Updated']
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