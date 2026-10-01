# Short Analysis Report
## Word Sense Disambiguation Using WordNet

### 1. Introduction
Word Sense Disambiguation (WSD) is the task of identifying the intended meaning of an ambiguous word from its context.

### 2. Objective
To identify different senses of ambiguous words using WordNet and apply a WSD algorithm to sample sentences.

### 3. Tools
- Python
- NLTK
- WordNet
- Pandas

### 4. Methodology
1. Obtain the possible senses of an ambiguous word from WordNet.
2. Extract WordNet definitions, synonyms, examples, hypernyms, and hyponyms.
3. Tokenize each sample sentence.
4. Apply the NLTK Lesk algorithm.
5. Record the predicted WordNet synset and definition.
6. Save the sense inventory and WSD results as CSV files.

### 5. WordNet
WordNet is a lexical database in which words are organized into synsets. It provides definitions and lexical relations including synonymy, hypernymy, and hyponymy.

### 6. Sample Ambiguous Words
- bank
- bat
- mouse
- crane
- plant

### 7. Results
The generated `output/sense_inventory.csv` contains the available WordNet senses and lexical relations. The generated `output/wsd_results.csv` contains the predicted sense for each sample sentence.

### 8. Analysis
Context helps distinguish different meanings of an ambiguous word. For example, words such as `money` and `deposit` provide financial context for `bank`, while `river` provides geographical context. The basic Lesk method uses lexical overlap and therefore may sometimes select an incorrect sense.

### 9. Limitations
- Basic Lesk relies on lexical overlap.
- WordNet definitions may not share words with the sentence context.
- Words with many senses are more difficult to disambiguate.
- The method does not deeply model sentence semantics.

### 10. Conclusion
The project demonstrates the use of WordNet for sense inventory creation, lexical relation exploration, and Word Sense Disambiguation. The experiment shows how context can be used to distinguish word meanings and also demonstrates the limitations of a simple dictionary-based WSD method.

### 11. Future Enhancement
A supervised classifier using Scikit-learn, contextual embeddings, or transformer-based representations can be added to improve WSD performance.
