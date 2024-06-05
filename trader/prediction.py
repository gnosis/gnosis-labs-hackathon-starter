import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from prediction_prophet.benchmark.agents import _make_prediction
from prediction_prophet.functions.create_embeddings_from_results import (
    create_embeddings_from_results,
)
from prediction_prophet.functions.generate_subqueries import generate_subqueries
from prediction_prophet.functions.prepare_report import prepare_report
from prediction_prophet.functions.scrape_results import scrape_results
from prediction_prophet.functions.search import search

DEFAULT_MODEL = "gpt-3.5-turbo-0125"


def research(
    goal: str,
    scrape_content_split_chunk_size: int = 800,
    scrape_content_split_chunk_overlap: int = 225,
    top_k_per_query: int = 8,
) -> str:
    with st.status("Generating subqueries"):
        # Generate subqueries out of the original question, to have more chances of finding relevant information.
        queries = generate_subqueries(query=goal, limit=5, model=DEFAULT_MODEL)
        st.write(f"Generated subqueries:" + "\n- " + "\n- ".join(queries))

    with st.status("Searching the web"):
        # For each subquery, do a search using Tavily.
        search_results = [r for _, r in search(queries)]

        if not search_results:
            raise ValueError(f"No search results found for the goal {goal}.")

        st.write(
            f"Found the following relevant results"
            + "\n- "
            + "\n- ".join(set(result.url for result in search_results))
        )

    with st.status(f"Scraping web results"):
        # Scrap content of each page.
        scraped = [
            result
            for result in scrape_results(search_results)
            if result.content.strip()
        ]
        st.write(f"Scraped content from {len(scraped)} websites")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", "  "],
        chunk_size=scrape_content_split_chunk_size,
        chunk_overlap=scrape_content_split_chunk_overlap,
    )

    with st.status(f"Performing similarity searches"):
        # Chunk scraped contents into chunks and create embeddings for them using OpenAI.
        collection = create_embeddings_from_results(scraped, text_splitter)
        st.write("Created embeddings")

        vector_result_texts: list[str] = []

        # For each subquery, do a similarity search against the chunks and collect the most relevant ones.
        for query in queries:
            top_k_per_query_results = collection.similarity_search(
                query, k=top_k_per_query
            )
            vector_result_texts += [
                result.page_content
                for result in top_k_per_query_results
                if result.page_content not in vector_result_texts
            ]
            st.write(f"Similarity searched for: {query}")

        st.write(f"Found {len(vector_result_texts)} relevant information chunks")

    with st.status(f"Preparing report"):
        # Prepare a report based on all relevant collected information.
        report = prepare_report(goal, vector_result_texts, model=DEFAULT_MODEL)
        st.markdown(report)

    return report


def predict(question: str) -> bool | None:
    """
    Customize this function to make a prediction about the question.

    You can keep using `research` and `_make_prediction` functions and just improve them, or create something new entirely.
    """
    # Create a report about the question.
    report = research(goal=question)
    # Make an informed prediction based on the report.
    prediction = _make_prediction(
        market_question=question,
        additional_information=report,
        engine=DEFAULT_MODEL,
        temperature=0.0,
    )
    # Answer yes if p_yes > 0.5, no otherwise.
    return (
        prediction.outcome_prediction.p_yes > 0.5
        if prediction.outcome_prediction
        else None
    )
