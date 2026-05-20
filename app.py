import streamlit as st
import tempfile
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS

from src.document_loader import extract_text_from_pdf
from src.text_processing import chunk_text
from src.entity_extraction import extract_entities
from src.retrieval_engine import RetrievalEngine
from src.clause_classifier import classify_chunks
from src.risk_engine import score_risk, risk_summary
from src.llm_service import generate_answer, generate_summary
from src.reporting import to_csv_bytes, build_processing_summary


st.set_page_config(
    page_title="Enterprise Document Intelligence",
    page_icon="📄",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0px;
    }
    .subtitle {
        color: #475569;
        font-size: 16px;
        margin-top: 4px;
        margin-bottom: 24px;
    }
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">Enterprise Document Intelligence Platform</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">AI-powered document review, clause analysis, entity extraction, retrieval-based Q&A, voice interaction, and risk summarization.</div>',
    unsafe_allow_html=True,
)


with st.sidebar:
    st.header("Configuration")

    retrieval_method = st.selectbox(
        "Search Engine",
        ["tfidf", "semantic"],
        format_func=lambda x: "Fast Keyword Search" if x == "tfidf" else "Semantic AI Search",
    )

    chunk_size = st.slider("Document Chunk Size", 400, 1200, 650, 50)
    overlap = st.slider("Chunk Overlap", 50, 250, 100, 10)
    top_k = st.slider("Retrieved Sections", 1, 6, 3, 1)

    enable_voice_output = st.toggle("Enable Voice Output", value=True)

    st.caption(
        "Use Fast Keyword Search for quick demos. Use Semantic AI Search for stronger meaning-based retrieval."
    )


if "processed" not in st.session_state:
    st.session_state.processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "executive_summary" not in st.session_state:
    st.session_state.executive_summary = ""

if "active_page" not in st.session_state:
    st.session_state.active_page = "Document Q&A"

if "last_audio_answer" not in st.session_state:
    st.session_state.last_audio_answer = ""


uploaded_files = st.file_uploader(
    "Upload business documents",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload text-based PDF documents such as contracts, agreements, policies, or business reports.",
)


if uploaded_files:
    if st.button("Analyze Documents", type="primary", use_container_width=False):
        combined_text = ""
        file_names = []

        with st.spinner("Analyzing uploaded documents..."):
            for file in uploaded_files:
                file_names.append(file.name)
                extracted = extract_text_from_pdf(file)
                combined_text += f"\n\n===== {file.name} =====\n\n{extracted}"

            if not combined_text.strip():
                st.error(
                    "No readable text was found in the uploaded PDFs. Please upload text-based PDF files."
                )
                st.stop()

            chunks = chunk_text(combined_text, chunk_size=chunk_size, overlap=overlap)
            entities_df = extract_entities(combined_text)

            retriever = RetrievalEngine(method=retrieval_method)
            active_method = retriever.build_index(chunks)

            clause_df = classify_chunks(chunks)

            risk_result = score_risk(combined_text)
            risk_text = risk_summary(risk_result)

            summary_df = build_processing_summary(
                file_count=len(file_names),
                chunk_count=len(chunks),
                entity_count=len(entities_df),
                clause_count=len(clause_df),
                retrieval_method=active_method,
            )

            st.session_state.file_names = file_names
            st.session_state.document_text = combined_text
            st.session_state.chunks = chunks
            st.session_state.entities_df = entities_df
            st.session_state.retriever = retriever
            st.session_state.active_method = active_method
            st.session_state.clause_df = clause_df
            st.session_state.risk_result = risk_result
            st.session_state.risk_text = risk_text
            st.session_state.summary_df = summary_df
            st.session_state.chat_history = []
            st.session_state.executive_summary = ""
            st.session_state.last_audio_answer = ""
            st.session_state.processed = True
            st.session_state.active_page = "Document Q&A"

        st.success("Document analysis completed successfully.")


def speak_answer(answer_text: str):
    try:
        clean_answer = answer_text.replace("#", "").replace("*", "")
        tts = gTTS(text=clean_answer, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
            tts.save(audio_file.name)
            st.audio(audio_file.name, format="audio/mp3")

    except Exception:
        st.info("Voice output is temporarily unavailable.")


if st.session_state.processed:
    risk = st.session_state.risk_result

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Documents", len(st.session_state.file_names))
    col2.metric("Text Sections", len(st.session_state.chunks))
    col3.metric("Entities", len(st.session_state.entities_df))
    col4.metric("Risk Level", risk["Risk Level"])

    st.divider()

    pages = [
        "Document Q&A",
        "Executive Summary",
        "Entity Intelligence",
        "Clause Analysis",
        "Risk Review",
    ]

    selected_page = st.radio(
        "Navigation",
        pages,
        horizontal=True,
        key="active_page",
        label_visibility="collapsed",
    )

    st.divider()

    if selected_page == "Document Q&A":
        st.markdown(
            '<div class="section-title">Document Q&A</div>',
            unsafe_allow_html=True,
        )
        st.write(
            "Ask questions about the uploaded documents using text or voice. Answers are grounded in retrieved document sections."
        )

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        st.subheader("Voice Input")
        voice_question = speech_to_text(
            language="en",
            use_container_width=True,
            just_once=True,
            key="voice_question_input",
        )

        typed_question = st.chat_input(
            "Ask about payment terms, termination, confidentiality, liability, risks..."
        )

        question = voice_question if voice_question else typed_question

        if question:
            st.session_state.chat_history.append(
                {"role": "user", "content": question}
            )

            retrieved = st.session_state.retriever.search(question, top_k=top_k)
            answer = generate_answer(question, retrieved, st.session_state.risk_text)

            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

            st.session_state.last_audio_answer = answer

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                st.write(answer)

                if enable_voice_output:
                    speak_answer(answer)

            with st.expander("Retrieved document evidence"):
                for item in retrieved:
                    st.markdown(
                        f"**Section ID:** {item['chunk_id']} | **Relevance Score:** {item['score']:.3f}"
                    )
                    st.write(item["text"][:1500])
                    st.divider()

    elif selected_page == "Executive Summary":
        st.markdown(
            '<div class="section-title">Executive Summary</div>',
            unsafe_allow_html=True,
        )
        st.write("Generate a business-friendly summary of the uploaded documents.")

        if st.button("Generate Executive Summary", type="primary"):
            entities_preview = st.session_state.entities_df.head(25).to_string(
                index=False
            )

            with st.spinner("Preparing executive summary..."):
                st.session_state.executive_summary = generate_summary(
                    st.session_state.document_text,
                    entities_preview,
                    st.session_state.risk_text,
                )

        if st.session_state.executive_summary:
            st.markdown(st.session_state.executive_summary)

            if enable_voice_output:
                st.subheader("Voice Output")
                speak_answer(st.session_state.executive_summary)

        st.subheader("Processing Summary")
        st.dataframe(st.session_state.summary_df, use_container_width=True)

    elif selected_page == "Entity Intelligence":
        st.markdown(
            '<div class="section-title">Entity Intelligence</div>',
            unsafe_allow_html=True,
        )
        st.write(
            "Automatically extracted dates, monetary values, percentages, emails, and business-critical terms."
        )

        st.dataframe(st.session_state.entities_df, use_container_width=True)

        st.download_button(
            "Download Entity Report",
            data=to_csv_bytes(st.session_state.entities_df),
            file_name="entity_intelligence_report.csv",
            mime="text/csv",
        )

    elif selected_page == "Clause Analysis":
        st.markdown(
            '<div class="section-title">Clause Analysis</div>',
            unsafe_allow_html=True,
        )
        st.write("Document sections classified into common business clause categories.")

        st.dataframe(st.session_state.clause_df, use_container_width=True)

        counts = (
            st.session_state.clause_df["Predicted Clause"]
            .value_counts()
            .reset_index()
        )
        counts.columns = ["Clause Type", "Count"]

        st.bar_chart(counts.set_index("Clause Type"))

        st.download_button(
            "Download Clause Report",
            data=to_csv_bytes(st.session_state.clause_df),
            file_name="clause_analysis_report.csv",
            mime="text/csv",
        )

    elif selected_page == "Risk Review":
        st.markdown(
            '<div class="section-title">Risk Review</div>',
            unsafe_allow_html=True,
        )

        risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)
        risk_col1.metric("Risk Level", risk["Risk Level"])
        risk_col2.metric("Risk Score", f"{risk['Risk Score']}/100")
        risk_col3.metric("High-Risk Terms", risk["High Risk Terms"])
        risk_col4.metric("Medium-Risk Terms", risk["Medium Risk Terms"])

        st.info(st.session_state.risk_text)

        st.write(
            "The risk review is generated using transparent keyword-based scoring. "
            "It is intended for business triage and should be validated by a human reviewer for final decisions."
        )

else:
    st.info("Upload PDF documents and click Analyze Documents to begin.")