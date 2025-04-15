# ECE1508_Group12Project

## Datasets
**Natural Questions Dataset** Original Repo [Click Here](https://github.com/google-research-datasets/natural-questions)

Kaggle has example preview: https://www.kaggle.com/datasets/validmodel/the-natural-questions-dataset

⚠️ The Final Test File: **dataset\gold_test_file_30.json**


## RAG Piplines

This project explored 4 RAG piplines:

1. Baseline RAG 1: using Fixed-Size Chunking
2. Baseline RAG 2: using Structured-Based Chunking
3. Two-Stage RAG 1: using Structured-Based Chunking + Sentence Window Chunking
4. Two-Stage RAG 2: using Structured-Based Chunking + Proposition Chunking

### Baseline RAG 1

Fxied Size Chunking using `RecursiveCharacterTextSplitter` in **.\Baseline_1.ipynb**

### Baseline RAG 2

### Two-Stage RAG 1

Stage 1 code file: **xxx**, the `FAISS` vector store created in this stage is stored in the folder **.\L1_vector_final**.  
Stage 2 code file: **.\Sentence_Window_Complete.ipynb**

### Two-Stage RAG 2
Stage 1 rely on teh structured chunking.  
Stage 2 code using **proposition** in **.\Proposition_Light.ipynb**

## Evaluataion

The code to calcualte the four evaluation criterias' score, generate complete evaluation result, including score distribution plot, mean value analysis and two question-type specific analysis in **.\Evaluation.ipynb**.

The detail evaluation result with detail output of each step(e.g. retrieved content and RAG generator's response to each question) can be find in folder **.\evaluation**
