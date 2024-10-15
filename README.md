# Comparative Analysis of Prompt Strategies for LLMs: Single-Task vs. Multitasking Prompts

This repository contains the code and datasets used for the paper *Comparative Analysis of Prompt Strategies for LLMs: Single-Task vs. Multitasking Prompts (Gozzi M., Di Maio F.)*. The study focuses on evaluating the performance of Large Language Models (LLMs) using both single-task and multitasking prompts, particularly in sentiment analysis and named entity recognition (NER).

## Repository Structure

The repository is organized as follows:

### Notebooks
The Jupyter notebooks used for data preparation, sampling, model evaluation, and result analysis can be found in the `./notebooks` folder:
- `01. Dataset production.ipynb`: Script for generating the dataset used in the study.
- `02. Sampling.ipynb`: Data sampling techniques.
- `02bis. Clean sample.ipynb`: Cleaning and filtering sampled data.
- `04. Single call.ipynb`: Script to process a single prompt call.
- `04bis. Multi call.ipynb`: Multi-prompt handling.
- `05. Dataset normalization.ipynb`: Data normalization steps.
- `06. Evaluation.ipynb`: Main evaluation script for model performance.
- `06b. Evaluation mono.ipynb`: Single-task evaluation script.
- `07. Statistics.ipynb`: Statistical analysis of the model results.

### Resources
All datasets and performance analysis results are stored in the `./resources` directory:
- Each subfolder under `resources` corresponds to one of the models evaluated, and contains:
  - Performance datasets (CSV files).
  - Visual performance analysis (PNG images).

The models analyzed include:
- `gemma2_9b`
- `llama3.1`
- `mistral7_b`
- `phi3_medium`
- `qwen2_7b`

## Dataset

The dataset used for the experiments consists of IMDB reviews with additional Named Entity Recognition (NER) annotations. The data was augmented using the SpaCy library and further processed for evaluation.

## Setup and Usage

### Requirements

All the requirements are defined on top of each notebook.

### Running the Notebooks

1. Clone the repository:
   ```bash
   git clone https://github.com/gozus19p/llm-benchmark.git
   cd llm-benchmark
   ```

2. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

3. Open and run the notebooks located in the `./notebooks` directory for the specific steps in the pipeline.

## Results and Evaluation

Results from the model evaluations, including performance metrics (e.g., F1 score for NER, BLEU score for text coherence), are stored in the respective model folders under `./resources`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
