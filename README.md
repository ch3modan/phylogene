# PhyloGene: Phylogenetic Tree Generator

PhyloGene is a command-line tool that automates the process of creating a phylogenetic tree from a set of related gene or protein sequences. It uses industry-standard tools to infer evolutionary relationships, providing a visual timeline of how different sequences have diverged.

This project uses Python, Biopython, and the external alignment tool Clustal Omega.

## Features

-   Performs a Multiple Sequence Alignment (MSA) on an input FASTA file.
-   Constructs a phylogenetic tree using the UPGMA method.
-   Outputs the alignment file, the tree in standard Newick format, and a high-quality PNG image of the tree.

## Prerequisites

This tool has an essential external dependency: **Clustal Omega**. You MUST install it and ensure it's available in your system's PATH.

-   **Linux (Ubuntu/Debian):**
    ```bash
    sudo apt-get update
    sudo apt-get install clustalo
    ```
-   **macOS (using Homebrew):**
    ```bash
    brew install clustal-omega
    ```
-   **Windows:** Download the executable from the [Clustal Omega website](http://www.clustal.org/omega/) and add its location to your system's PATH environment variable.

To verify the installation, open a new terminal and type `clustalo --version`. You should see the version number.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [URL_to_your_new_GitHub_repo]
    cd phylogene
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the tool from the command line, providing the path to your multi-sequence FASTA file.

**Command:**
```bash
python phylogene.py sample_genes.fasta --output_dir my_analysis_results
```

This will create a directory named `my_analysis_results` containing the output.

### Example Output

After running the command, you will find the following files in your output directory:

1.  **`aligned_sequences.fasta`**: The result of the multiple sequence alignment.
2.  **`phylogenetic_tree.nwk`**: The tree structure in Newick format, which can be used in other phylogenetic software.
    ```
    (Yeast_Cytochrome_C:0.2, (Horse_Cytochrome_C:0.1, (Macaque_Cytochrome_C:0.05, (Human_Cytochrome_C:0.0, Chimpanzee_Cytochrome_C:0.0):0.05):0.05):0.1);
    ```
3.  **`phylogenetic_tree.png`**: A visual representation of the tree. The shorter the branches, the more closely related the sequences are.

![Example Tree](https://i.imgur.com/a/AGMorhq.png)

## License
This project is licensed under the MIT License.
