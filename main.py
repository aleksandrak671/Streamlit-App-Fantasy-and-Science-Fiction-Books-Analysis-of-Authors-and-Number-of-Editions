from data_loader import load_books_json
from processing import prepare_dataframe, clean_data, average_rating_by_genre
from visualization import plot_boxplot_ratings

def main():
    data = load_books_json()
    df = prepare_dataframe(data)
    stats = average_rating_by_genre(df)
    print(stats)
    plot_boxplot_ratings(df)

if __name__ == "__main__":
    main()
