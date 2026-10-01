# Word Sense Disambiguation Using WordNet

## Objective
Develop a Word Sense Disambiguation (WSD) system using NLTK WordNet and lexical relations.

## Expected Outcomes
- Identify different senses of ambiguous words.
- Explore WordNet lexical relations.
- Apply a WSD algorithm to sample sentences.

## Algorithm
This project uses the simplified Lesk algorithm available in NLTK. It compares the context of an ambiguous word with WordNet sense definitions.

## Project Structure

WSD_WordNet_Project/
├── wsd.py
├── requirements.txt
├── sample_sentences.txt
├── README.md
├── output/
│   ├── sense_inventory.csv
│   └── wsd_results.csv
└── report/
    └── WSD_Report.md

## Installation

```powershell
python -m pip install -r requirements.txt
```

The program automatically downloads required NLTK resources.

## Run

```powershell
python wsd.py
```

## Ambiguous Words
- bank
- bat
- mouse
- crane
- plant

## Deliverables
1. Sense inventory: `output/sense_inventory.csv`
2. WSD results: `output/wsd_results.csv`
3. Python implementation: `wsd.py`
4. Short analysis report: `report/WSD_Report.md`

## Important Note
The basic Lesk algorithm is a lexical-overlap method and may occasionally select an incorrect sense. This is useful for discussing limitations and possible improvements.


## Frontend

This project includes a Streamlit web interface in `app.py`.

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the frontend:

```powershell
python -m streamlit run app.py
```

The browser will open the WSD application. If it does not open automatically, use the local URL shown in the terminal, usually:

`http://localhost:8501`

### Frontend Features
- WSD Demo: enter a sentence and ambiguous word.
- Sense Inventory: explore all WordNet senses.
- WSD Results: view generated CSV results.
- Lexical Relations: explore synonyms, hypernyms, hyponyms, and examples.


## Frontend Fixes
The latest `app.py` includes fixes for:
- `NameError: name 'os' is not defined`
- `TypeError: cannot pickle '_thread.RLock' object`

The Lexical Relations page now passes synset names (strings) to Streamlit widgets and reconstructs the WordNet synset after selection.

## Start Frontend
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
