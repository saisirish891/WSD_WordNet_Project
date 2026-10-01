import os
import nltk
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_resources():
    resources = ["wordnet", "omw-1.4", "punkt", "punkt_tab"]
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass

def get_senses(word):
    records = []
    for i, synset in enumerate(wn.synsets(word), start=1):
        records.append({
            "word": word,
            "sense_number": i,
            "synset": synset.name(),
            "part_of_speech": synset.pos(),
            "definition": synset.definition(),
            "synonyms": ", ".join(
                lemma.name().replace("_", " ") for lemma in synset.lemmas()
            ),
            "examples": "; ".join(synset.examples()),
            "hypernyms": ", ".join(
                h.name().replace("_", " ") for h in synset.hypernyms()
            ),
            "hyponyms": ", ".join(
                h.name().replace("_", " ") for h in synset.hyponyms()
            )
        })
    return records

def perform_wsd(sentence, ambiguous_word):
    tokens = word_tokenize(sentence)
    sense = lesk(tokens, ambiguous_word.lower())
    if sense is None:
        return {
            "sentence": sentence,
            "word": ambiguous_word,
            "predicted_sense": "No sense found",
            "definition": "No matching WordNet sense found",
            "synonyms": ""
        }
    return {
        "sentence": sentence,
        "word": ambiguous_word,
        "predicted_sense": sense.name(),
        "definition": sense.definition(),
        "synonyms": ", ".join(
            lemma.name().replace("_", " ") for lemma in sense.lemmas()
        )
    }

def main():
    download_resources()

    ambiguous_words = ["bank", "bat", "mouse", "crane", "plant"]

    all_senses = []
    for word in ambiguous_words:
        all_senses.extend(get_senses(word))

    pd.DataFrame(all_senses).to_csv(
        os.path.join(OUTPUT_DIR, "sense_inventory.csv"), index=False
    )

    test_data = [
        ("I went to the bank to deposit money.", "bank"),
        ("The fisherman sat on the bank of the river.", "bank"),
        ("The bat flew out of the cave at night.", "bat"),
        ("The baseball player hit the ball with a bat.", "bat"),
        ("The computer mouse stopped working.", "mouse"),
        ("The mouse ran across the kitchen floor.", "mouse"),
        ("The crane lifted the heavy container.", "crane"),
        ("The crane stood near the lake.", "crane"),
        ("The workers planted a tree in the garden.", "plant"),
        ("The factory plant produces electronic components.", "plant")
    ]

    results = [perform_wsd(sentence, word) for sentence, word in test_data]

    pd.DataFrame(results).to_csv(
        os.path.join(OUTPUT_DIR, "wsd_results.csv"), index=False
    )

    print("WSD project completed successfully.")
    print("Generated:")
    print("- output/sense_inventory.csv")
    print("- output/wsd_results.csv")

if __name__ == "__main__":
    main()
