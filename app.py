import streamlit as st
import matplotlib.pyplot as plt
from data_loader import load_books_json
from processing import (
    compose_pipeline,
    sample_titles_by_genre
)
from visualization import (
    plot_boxplot_ratings,
    plot_violin_ratings,
    plot_top_books_per_author,
    plot_boxplot_interactive
)

st.set_page_config(layout="wide")
st.title("📚 Książki fantasy – analiza autorów i liczby wydań")

with st.spinner("🔄 Ładowanie danych z OpenLibrary..."):
    fantasy_data, scifi_data = load_books_json()
    df, stats, df_filtered, genre_stats, genre_freq = compose_pipeline(fantasy_data, scifi_data)

# 1. średnia liczba wydań
st.subheader("⭐ Średnia liczba wydań na autora")
if stats.empty:
    st.warning("Brak danych do wyświetlenia.")
else:
    st.bar_chart(stats.set_index("Author"))
    st.dataframe(stats)

# 2. średnia i odchylenie
st.subheader("📏 Średnia i odchylenie liczby wydań")
genre_stats = genre_stats.sort_values(by='Średnia', ascending=False)
st.dataframe(genre_stats)

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(genre_stats['Author'], genre_stats['Średnia'], yerr=genre_stats['Odchylenie'], capsize=5)
ax.set_ylabel("Średnia liczba wydań")
ax.set_title("Średnia liczba wydań i odchylenie – Top 15 autorów")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

# 3. najczęściej publikujący autorzy
st.subheader("📊 Najczęściej publikujący autorzy")
st.bar_chart(genre_freq.set_index("Author"))

# 4. boxplot + interaktywny boxplot
st.subheader("📦 Rozkład liczby wydań")
plot_boxplot_ratings(df_filtered)

st.subheader("📦 Interaktywny boxplot liczby wydań")
plot_boxplot_interactive(df, max_authors=15, max_y=200)

# 5. violin plot
st.subheader("🎻 Gęstość wydań (violin plot)")
plot_violin_ratings(df_filtered)

# 6. top książki
st.subheader("🏆 Top 3 książki najpopularniejszych autorów")
plot_top_books_per_author(df, top_n=3, max_authors=6)

# 7. przykładowe książki wybranego autora
st.subheader("📖 Przykładowe książki danego autora")
author_choice = st.selectbox("Wybierz autora:", stats['Author'])
sample_titles = sample_titles_by_genre(df, author_choice)
for title in sample_titles:
    st.write("•", title)

# 8. Fantasy + SciFi
st.subheader("🧬 Książki fantasy zaklasyfikowane także jako science fiction")
scifi_cross = df[df['in_scifi'] == True][['title', 'authors']].drop_duplicates()
st.dataframe(scifi_cross.head(20))

# 9. porównanie wydań: Fantasy vs Fantasy + SciFi
st.subheader("📊 Porównanie średniej liczby wydań")
scifi_compare = df.groupby('in_scifi')['edition_count'].agg(['mean', 'count']).reset_index()
scifi_compare['in_scifi'] = scifi_compare['in_scifi'].map({True: 'Fantasy + Sci-Fi', False: 'Tylko Fantasy'})

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(scifi_compare['in_scifi'], scifi_compare['mean'], color=['#4CAF50', '#2196F3'])
ax.set_ylabel("Średnia liczba wydań")
ax.set_title("Średnia liczba wydań – Fantasy vs Fantasy + Sci-Fi")

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center')

st.pyplot(fig)
