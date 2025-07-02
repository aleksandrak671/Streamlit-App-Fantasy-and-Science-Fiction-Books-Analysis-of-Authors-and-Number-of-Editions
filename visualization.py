import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import streamlit as st


def plot_boxplot_ratings(df, max_y=200):
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(data=df, x='authors', y='edition_count')
    plt.xticks(rotation=45, ha='right')
    plt.title("📦 Boxplot liczby wydań wg autora (bez ekstremów)")
    ax.set_ylim(0, max_y)  # ograniczenie górnej granicy
    plt.tight_layout()
    st.pyplot(plt)

def plot_boxplot_interactive(df, max_authors=15, max_y=200):
    top_authors = df['authors'].value_counts().head(max_authors).index
    df_top = df[df['authors'].isin(top_authors)].copy()

    fig = px.box(
        df_top,
        x="authors",
        y="edition_count",
        points="outliers",
        title="📦 Interaktywny boxplot liczby wydań wg autora (max {} wydań)".format(max_y),
        labels={"edition_count": "Liczba wydań", "authors": "Autor"}
    )

    fig.update_layout(
        xaxis_tickangle=45,
        yaxis_range=[0, max_y],
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_violin_ratings(df):
    plt.figure(figsize=(12, 6))
    ax = sns.violinplot(data=df, x='authors', y='edition_count', inner='quartile')
    ax.set_yscale('log')  # oś Y w skali logarytmicznej
    plt.xticks(rotation=45, ha='right')
    plt.title("Gęstość liczby wydań wg autora (skala logarytmiczna)")
    plt.ylabel("Liczba wydań (log scale)")
    plt.tight_layout()
    st.pyplot(plt)

def plot_top_books_per_author(df, top_n=3, max_authors=6):
    # ograniczenie do najpopularniejszych autorów
    top_authors = df['authors'].value_counts().head(max_authors).index
    df = df[df['authors'].isin(top_authors)]

    df_grouped = df.groupby(['authors', 'title'])['edition_count'].mean().reset_index()
    top_books = df_grouped.groupby('authors').apply(lambda x: x.nlargest(top_n, 'edition_count')).reset_index(drop=True)

    g = sns.FacetGrid(top_books, col="authors", col_wrap=3, height=4, sharex=False, sharey=False)
    g.map_dataframe(sns.barplot, x="edition_count", y="title", orient="h", palette="viridis")
    g.set_titles("{col_name}")
    g.set_axis_labels("Liczba wydań", "Tytuł")
    plt.tight_layout()
    st.pyplot(g.figure)


def plot_top_books_per_author(df, top_n=3, max_authors=6):
    # najpopularniejsi autorzy
    top_authors = df['authors'].value_counts().head(max_authors).index
    df = df[df['authors'].isin(top_authors)]

    # top N książek na autora wg liczby wydań
    grouped = df.groupby(['authors', 'title'])['edition_count'].mean().reset_index()
    top_books = grouped.groupby('authors').apply(lambda x: x.nlargest(top_n, 'edition_count')).reset_index(drop=True)

    # interaktywny wykres
    fig = px.bar(
        top_books,
        x='edition_count',
        y='title',
        color='authors',
        orientation='h',
        hover_data={'edition_count': True, 'title': True, 'authors': True},
        labels={'edition_count': 'Liczba wydań', 'title': 'Tytuł', 'authors': 'Autor'},
        title="Top 3 książki każdego z najpopularniejszych autorów"
    )
    fig.update_layout(barmode='group', height=600)
    st.plotly_chart(fig, use_container_width=True)
