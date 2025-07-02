import pandas as pd

def prepare_dataframe(fantasy_data, scifi_data):
    df = pd.DataFrame(fantasy_data)
    required_cols = ['title', 'authors', 'edition_count', 'first_publish_year']
    df = df[[col for col in required_cols if col in df.columns]]
    
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    df['authors'] = df['authors'].apply(lambda x: [a['name'] for a in x] if isinstance(x, list) else [])
    df = df.explode('authors')
    df = df.dropna(subset=['title', 'authors', 'edition_count', 'first_publish_year'])
    df['edition_count'] = pd.to_numeric(df['edition_count'], errors='coerce')

    scifi_titles = pd.DataFrame(scifi_data)[['title']]
    scifi_titles['in_scifi'] = True
    df = df.merge(scifi_titles, on='title', how='left')
    df['in_scifi'] = df['in_scifi'].fillna(False)

    return df

def average_rating_by_genre(df):
    return df.groupby('authors')['edition_count'].mean().reset_index().rename(columns={
        'authors': 'Author', 'edition_count': 'Average Editions'
    })

def genre_rating_stats(df):
    grouped = df.groupby('authors')['edition_count']
    return grouped.agg(['mean', 'std']).reset_index().rename(columns={
        'authors': 'Author', 'mean': 'Średnia', 'std': 'Odchylenie'
    })

def sample_titles_by_genre(df, author, n=5):
    sample = df[df['authors'] == author]['title']
    return sample.sample(n=min(n, len(sample))).tolist()

def genre_frequency(df):
    freq = df['authors'].value_counts().reset_index()
    freq.columns = ['Author', 'Count']
    return freq.head(15)

# złożenie funkcji
def compose_pipeline(fantasy_data, scifi_data):
    df = prepare_dataframe(fantasy_data, scifi_data)
    stats = average_rating_by_genre(df)
    top_authors = df['authors'].value_counts().head(15).index
    df_filtered = df[df['authors'].isin(top_authors)]
    genre_stats = genre_rating_stats(df_filtered)
    genre_freq = genre_frequency(df)
    return df, stats, df_filtered, genre_stats, genre_freq
