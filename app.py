import os
import streamlit as st
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

st.set_page_config(
    page_title="Word Sense Disambiguation",
    page_icon="🧠",
    layout="wide"
)

@st.cache_resource
def setup_nltk():
    resources = ["wordnet", "omw-1.4", "punkt", "punkt_tab"]
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass

setup_nltk()

st.title("🧠 Word Sense Disambiguation using WordNet")
st.write(
    "Enter a sentence and an ambiguous word. The system uses "
    "WordNet and the Lesk algorithm to predict the intended sense."
)

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["WSD Demo", "Sense Inventory", "WSD Results", "Lexical Relations"]
)


def get_wsd(sentence, word):
    tokens = word_tokenize(sentence)
    return lesk(tokens, word.lower())


def relation_names(synsets):
    return [s.name() for s in synsets]


# ---------------------------------------------------------
# WSD DEMO
# ---------------------------------------------------------
if page == "WSD Demo":
    st.header("🔍 Word Sense Disambiguation")

    sentence = st.text_area(
        "Enter a sentence",
        "I went to the bank to deposit money."
    )

    word = st.text_input("Ambiguous word", "bank")

    if st.button("Disambiguate", type="primary"):
        if not sentence.strip() or not word.strip():
            st.warning("Please enter both a sentence and a word.")
        else:
            sense = get_wsd(sentence, word)

            if sense:
                st.success("Sense identified")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Predicted Sense")
                    st.info(sense.name())

                with col2:
                    st.subheader("Definition")
                    st.write(sense.definition())

                st.subheader("Synonyms")
                st.write(
                    ", ".join(
                        lemma.name().replace("_", " ")
                        for lemma in sense.lemmas()
                    )
                )

                examples = sense.examples()
                if examples:
                    st.subheader("WordNet Examples")
                    for example in examples:
                        st.write("•", example)

                st.subheader("Lexical Relations")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Hypernyms**")
                    hypernyms = sense.hypernyms()
                    if hypernyms:
                        for item in hypernyms[:15]:
                            st.write("•", item.name().replace("_", " "))
                    else:
                        st.write("No hypernyms found.")

                with col2:
                    st.write("**Hyponyms**")
                    hyponyms = sense.hyponyms()
                    if hyponyms:
                        for item in hyponyms[:15]:
                            st.write("•", item.name().replace("_", " "))
                    else:
                        st.write("No hyponyms found.")
            else:
                st.error("No matching WordNet sense was found.")


# ---------------------------------------------------------
# SENSE INVENTORY
# ---------------------------------------------------------
elif page == "Sense Inventory":
    st.header("📚 WordNet Sense Inventory")

    word = st.text_input("Enter a word", "bank", key="inventory_word")

    if st.button("Find Senses"):
        synsets = wn.synsets(word)

        if not synsets:
            st.warning("No senses found in WordNet.")
        else:
            records = []

            for i, synset in enumerate(synsets, 1):
                records.append({
                    "Sense": i,
                    "Synset": synset.name(),
                    "POS": synset.pos(),
                    "Definition": synset.definition(),
                    "Synonyms": ", ".join(
                        lemma.name().replace("_", " ")
                        for lemma in synset.lemmas()
                    )
                })

            df = pd.DataFrame(records)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Sense Inventory",
                csv,
                "sense_inventory.csv",
                "text/csv"
            )


# ---------------------------------------------------------
# WSD RESULTS
# ---------------------------------------------------------
elif page == "WSD Results":
    st.header("📊 WSD Results")

    path = os.path.join("output", "wsd_results.csv")

    if os.path.exists(path):
        df = pd.read_csv(path)

        st.metric("Number of Test Sentences", len(df))
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download WSD Results",
            csv,
            "wsd_results.csv",
            "text/csv"
        )
    else:
        st.warning("Run `python wsd.py` first to generate the results.")


# ---------------------------------------------------------
# LEXICAL RELATIONS
# ---------------------------------------------------------
elif page == "Lexical Relations":
    st.header("🔗 WordNet Lexical Relations")

    word = st.text_input("Enter a word", "bat", key="relation_word")

    if st.button("Explore Relations"):
        synsets = wn.synsets(word)

        if not synsets:
            st.warning("No WordNet entries found.")
        else:
            # IMPORTANT:
            # Streamlit selectbox receives strings instead of Synset objects.
            # This prevents "cannot pickle '_thread.RLock' object".
            synset_names = [s.name() for s in synsets]

            selected_name = st.selectbox(
                "Select a sense",
                synset_names,
                format_func=lambda name: f"{name} — {wn.synset(name).definition()}"
            )

            selected = wn.synset(selected_name)

            st.subheader("Definition")
            st.write(selected.definition())

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Synonyms")
                for lemma in selected.lemmas():
                    st.write("•", lemma.name().replace("_", " "))

                st.subheader("Hypernyms")
                hypernyms = selected.hypernyms()
                if hypernyms:
                    for item in hypernyms[:20]:
                        st.write("•", item.name().replace("_", " "))
                else:
                    st.write("No hypernyms found.")

            with col2:
                st.subheader("Hyponyms")
                hyponyms = selected.hyponyms()
                if hyponyms:
                    for item in hyponyms[:20]:
                        st.write("•", item.name().replace("_", " "))
                else:
                    st.write("No hyponyms found.")

                st.subheader("Examples")
                examples = selected.examples()
                if examples:
                    for example in examples:
                        st.write("•", example)
                else:
                    st.write("No examples available.")

st.sidebar.markdown("---")
st.sidebar.caption("WSD Project | NLTK WordNet + Lesk")
