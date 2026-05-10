# Structural Profile HMM for Kunitz Domain Discovery

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![HMMER](https://img.shields.io/badge/HMMER-3.3-green.svg)
![US-align](https://img.shields.io/badge/US--align-v1.1-orange.svg)
![MMseqs2](https://img.shields.io/badge/MMseqs2-latest-red.svg)

## Overview
This repository contains a high-precision structural bioinformatics pipeline designed to robustly identify Kunitz (BPTI) domains. Traditional sequence searches (e.g., BLAST) often yield high False Positive rates when dealing with evolutionary diverged domains. This project overcomes sequence decay by anchoring a **Profile Hidden Markov Model (HMM)** entirely on 3D structural superpositions, achieving **100% specificity** against the human proteome.

## 🚀 Key Features
* **Structure-First MSA:** Utilizes 3D spatial alignment rather than sequence identity to map conserved motifs (the 6-cysteine scaffold and GPC active site).
* **Automated Star Alignment:** Custom Python scripts to merge variable-length pairwise `US-align` outputs into strict 2D matrices required for HMM building.
* **Gold-Standard Benchmarking:** Includes an automated 2-Fold Cross-Validation pipeline to calculate true operational metrics (Accuracy, MCC) across varying E-value thresholds.

## 🛠️ Pipeline & Code Sections Description

The repository is divided into sequential stages that follow the bioinformatics pipeline:

### `1_Data_Curation/`
Contains the raw FASTA datasets fetched from Swiss-Prot.
* **`pos_non_human_bpti.fasta`**: 380 manually reviewed Kunitz domains from non-human taxa (ticks, snakes, anemones). (Positive Test Set)
* **`neg_human_non_bpti.fasta`**: ~20,414 human proteins lacking the Kunitz domain. (Negative Test Set)

### `2_Baseline_BLAST/`
Contains the baseline scripts establishing the limitations of sequence alignment. Running BLAST on the negative set yields ~551 False Positives, defining the benchmark our HMM must beat.

### `3_Clustering_MMseqs2/`
* **`cluster_chains.sh`**: Uses MMseqs2 with strict parameters (`-c 0.95 --min-seq-id 0.90`) to reduce redundancy in our seed data, resulting in highly representative, diverse centroids for modeling.

### `4_Structural_Alignment/`
* **`usalign_star_msa.py`**: The core custom script of the project. It loops through the PDB files of our cluster centroids, designates a master reference, and runs `US-align` to perform 3D rigid-body superpositions. It then mathematically parses the pairwise alignments, calculates required structural insertions/deletions, and generates a structurally true, gap-padded `kunitz_structural_msa_fixed.fasta`.

### `5_HMM_Modeling/`
* **`build_and_search.sh`**: Executes the HMMER suite. Uses `hmmbuild` to translate the structural MSA into `kunitz_profile.hmm`. Runs `hmmsearch` with the `--max` (no heuristic filters) and `-Z 20794` (normalized search space) flags against both test sets.

### `6_Evaluation_and_Metrics/`
Contains the performance evaluation loop and cross-validation tools.
* **`cross_validation_split.py`**: A robust data-handling script that shuffles matches and non-matches, defines True Negatives using the `comm` command, and splits the data into `kunitz_set_1.txt` and `kunitz_set_2.txt` to prevent distribution bias.
* **`performance.py`**: Calculates the Confusion Matrix, Accuracy, and Matthews Correlation Coefficient (MCC) based on the structural search outputs. 
* **`plot_metrics.py`**: Generates matplotlib visualizations of MCC vs. E-value thresholds to identify the optimal operational parameter.

## ⚙️ Installation & Dependencies

To run this pipeline locally or in Google Colab, you require the following dependencies:

```bash
# Install HMMER
sudo apt-get install hmmer

# Install MMseqs2
conda install -c conda-forge -c bioconda mmseqs2

# Compile US-align
wget [https://zhanggroup.org/US-align/bin/module/USalign.cpp](https://zhanggroup.org/US-align/bin/module/USalign.cpp)
g++ -O3 -ffast-math -lm -o USalign USalign.cpp
