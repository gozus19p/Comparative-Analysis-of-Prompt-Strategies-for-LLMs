# Comparative Analysis of Prompt Strategies for Large Language Models: Single-Task vs. Multitask Prompts

[![DOI](https://img.shields.io/badge/DOI-10.3390%2Felectronics13234712-blue)](https://doi.org/10.3390/electronics13234712)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3-blue.svg)](requirements.txt)

This repository contains the code and datasets for the paper:

> Gozzi, M.; Di Maio, F. *Comparative Analysis of Prompt Strategies for Large Language Models: Single-Task vs. Multitask Prompts.* **Electronics** 2024, *13*, 4712. [https://doi.org/10.3390/electronics13234712](https://doi.org/10.3390/electronics13234712)

## About

The study investigates the effectiveness of prompt engineering strategies for Large Language Models (LLMs), comparing **single-task** and **multitask** prompts. Specifically, it analyzes whether a single prompt handling multiple tasks — named entity recognition (NER), sentiment analysis, and JSON output formatting — can achieve performance comparable to dedicated single-task prompts.

The claims are validated with statistical analyses, including paired Wilcoxon tests, McNemar tests, and Friedman tests. Experiments were conducted on five open-weight LLMs:

| Model | Size |
| --- | --- |
| Llama 3.1 | 8B |
| Qwen2 | 7B |
| Mistral | 7B |
| Phi-3 | Medium (14B) |
| Gemma2 | 9B |

The results indicate that there is no definitive rule favoring single-task prompts over multitask prompts; rather, their relative performance is highly contingent on the specific model's data and architecture.

## Repository Structure

```
.
|-- notebooks/                    # End-to-end experimental pipeline (Jupyter)
|   |-- 01. Dataset production.ipynb
|   |-- 02. Sampling.ipynb
|   |-- 02bis. Clean sample.ipynb
|   |-- 04. Single call.ipynb
|   |-- 04bis. Multi call.ipynb
|   |-- 05. Dataset normalization.ipynb
|   |-- 06. Evaluation.ipynb
|   |-- 07. Statistics.ipynb
|-- runners/                      # Standalone scripts for the LLM inference calls
|   |-- 04. Single call.py
|   |-- 04bis. Multi call.py
|-- resources/
|   |-- IMDB Dataset Sampled.csv  # Sampled dataset used in the experiments
|   |-- statistics.csv             # Aggregated performance statistics
|   |-- statistics-revised.csv
|   |-- gemma2_9b/                # Per-model results (CSV + PNG)
|   |-- llama3.1/
|   |-- mistral_7b/
|   |-- phi3_medium/
|   |-- qwen2_7b/
|-- statistics.xlsx               # Summary of the statistical analyses
|-- requirements.txt
```

### Notebooks

The Jupyter notebooks cover data preparation, sampling, model evaluation, and result analysis:

- `01. Dataset production.ipynb` — generation of the dataset used in the study.
- `02. Sampling.ipynb` — data sampling techniques.
- `02bis. Clean sample.ipynb` — cleaning and filtering of sampled data.
- `04. Single call.ipynb` — processing with single-task prompts.
- `04bis. Multi call.ipynb` — processing with multitask prompts.
- `05. Dataset normalization.ipynb` — data normalization steps.
- `06. Evaluation.ipynb` — evaluation of model performance.
- `07. Statistics.ipynb` — statistical analysis of the model results.

### Runners

The `runners/` directory contains standalone Python versions of the two inference steps, for executing the single-task and multitask prompt calls outside of a notebook environment.

### Resources

Each subfolder of `resources/` corresponds to one of the evaluated models and contains the performance datasets (CSV files) and visual performance analyses (PNG images). The aggregated statistics are available in `statistics.csv`, `statistics-revised.csv`, and `statistics.xlsx`.

## Dataset

The dataset consists of IMDB movie reviews augmented with named entity recognition (NER) annotations, generated with the [spaCy](https://spacy.io/) library and further processed for evaluation. The sampled dataset used in the experiments is available in `resources/IMDB Dataset Sampled.csv`.

## Setup and Usage

### Requirements

The Python dependencies are listed in `requirements.txt` (each notebook also states its requirements at the top). Install them with:

```bash
pip install -r requirements.txt
```

### Running the Pipeline

1. Clone the repository:

   ```bash
   git clone https://github.com/gozus19p/Comparative-Analysis-of-Prompt-Strategies-for-LLMs.git
   cd Comparative-Analysis-of-Prompt-Strategies-for-LLMs
   ```

2. Start Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

3. Open and run the notebooks in `notebooks/` in numbered order to reproduce the pipeline (dataset production, sampling, inference, evaluation, statistics).

## Results and Evaluation

Results from the model evaluations, including performance metrics (e.g., F1 score for NER, BLEU and ROUGE scores for text coherence), are stored in the respective model folders under `resources/`. The statistical analyses supporting the paper's conclusions are in `statistics.xlsx` and the `07. Statistics.ipynb` notebook.

## Citation

If you use this code or dataset in your research, please cite the paper:

**APA**

> Gozzi, M., & Di Maio, F. (2024). Comparative Analysis of Prompt Strategies for Large Language Models: Single-Task vs. Multitask Prompts. *Electronics*, *13*(23), 4712. https://doi.org/10.3390/electronics13234712

**BibTeX**

```bibtex
@article{Gozzi2024,
  author       = {Gozzi, Manuel and Di Maio, Federico},
  title        = {Comparative Analysis of Prompt Strategies for Large Language Models: Single-Task vs. Multitask Prompts},
  journal      = {Electronics},
  volume       = {13},
  number       = {23},
  article-number = {4712},
  year         = {2024},
  issn         = {2079-9292},
  doi          = {10.3390/electronics13234712},
  url          = {https://www.mdpi.com/2079-9292/13/23/4712},
  publisher    = {MDPI}
}
```

Citation metadata is also available in [CITATION.cff](CITATION.cff), which is picked up by GitHub's *"Cite this repository"* feature.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
