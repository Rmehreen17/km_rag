import streamlit as st
from src.rag_pipeline import RAGPipeline

st.set_page_config(
    page_title="Enterprise Knowledge Search",
    page_icon="🔎",
    layout="wide"
)

st.title("Enterprise Knowledge Search")

st.markdown(
    "Ask questions across enterprise documents and get answers "
    "grounded in the underlying evidence."
)

@st.cache_resource
def load_pipeline():
    return RAGPipeline()

pipeline = load_pipeline()

query = st.text_input(
    "Ask a question",
    placeholder="e.g. How does Microsoft approach responsible AI?"
)

if query:
    with st.spinner("Searching the knowledge base..."):
        result = pipeline.ask(query)

    st.subheader("Answer")
    st.write(result["answer"])

    st.divider()

    if result["abstained"]:

        st.subheader("Evidence")
        st.info(
            "No supporting evidence was found in the provided corpus."
        )

    else:

        st.subheader("Sources & Evidence")

        for i, source in enumerate(
            result["retrieved_evidence"],
            start=1
        ):

            with st.expander(
                f"{i}. {source['document']} · "
                f"Page {source['page']} · "
                f"{source['chunk_id']}"
            ):
                st.write(source["text"])
