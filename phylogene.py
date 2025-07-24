import argparse
import os
import sys
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio import Phylo, AlignIO
import matplotlib
import matplotlib.pyplot as plt

# Use a non-interactive backend for Matplotlib to prevent it from trying to open a GUI window.
matplotlib.use('Agg')

def check_tool_installed(tool_name):
    """Check whether `tool_name` is on PATH and executable."""
    from shutil import which
    return which(tool_name) is not None

def run_phylogenetic_analysis(fasta_file, output_dir):
    """
    Runs the full phylogenetic analysis pipeline.
    1. Performs Multiple Sequence Alignment using Clustal Omega.
    2. Builds a phylogenetic tree from the alignment.
    3. Saves the tree as a Newick file and a PNG image.

    Args:
        fasta_file (str): Path to the input multi-sequence FASTA file.
        output_dir (str): Directory to save the output files.
    """
    # --- Step 0: Validate inputs and prerequisites ---
    if not check_tool_installed("clustalo"):
        print("ERROR: Clustal Omega ('clustalo') is not installed or not in your system's PATH.")
        print("Please install it from http://www.clustal.org/omega/ or via a package manager (e.g., 'sudo apt-get install clustalo').")
        sys.exit(1)

    if not os.path.exists(fasta_file):
        print(f"ERROR: Input file not found at '{fasta_file}'")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    print(f"Output will be saved to '{output_dir}' directory.")

    # Define output file paths
    aligned_fasta_path = os.path.join(output_dir, "aligned_sequences.fasta")
    tree_newick_path = os.path.join(output_dir, "phylogenetic_tree.nwk")
    tree_png_path = os.path.join(output_dir, "phylogenetic_tree.png")

    # --- Step 1: Multiple Sequence Alignment ---
    print("\nStep 1: Running Multiple Sequence Alignment with Clustal Omega...")
    try:
        clustalo_cline = ClustalOmegaCommandline(
            infile=fasta_file,
            outfile=aligned_fasta_path,
            force=True,  # Overwrite output file if it exists
            verbose=True,
            auto=True
        )
        stdout, stderr = clustalo_cline()
        print("Alignment complete.")
    except Exception as e:
        print(f"An error occurred during Clustal Omega execution: {e}")
        sys.exit(1)

    # --- Step 2: Phylogenetic Tree Construction ---
    print("\nStep 2: Building phylogenetic tree...")
    try:
        # Read the alignment
        aln = AlignIO.read(aligned_fasta_path, "fasta")

        # Import necessary modules for tree construction
        from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

        # Calculate the distance matrix
        calculator = DistanceCalculator('identity')
        dist_matrix = calculator.get_distance(aln)

        # Construct the tree using UPGMA (Unweighted Pair Group Method with Arithmetic Mean)
        constructor = DistanceTreeConstructor(calculator, 'upgma')
        tree = constructor.build_tree(aln)
        tree.rooted = True # UPGMA creates a rooted tree

        # Save the tree in Newick format
        Phylo.write(tree, tree_newick_path, "newick")
        print(f"Tree saved in Newick format to '{tree_newick_path}'")

    except Exception as e:
        print(f"An error occurred during tree construction: {e}")
        sys.exit(1)

    # --- Step 3: Visualize and Save the Tree ---
    print("\nStep 3: Visualizing tree and saving to PNG...")
    try:
        fig = plt.figure(figsize=(10, 8), dpi=100)
        axes = fig.add_subplot(1, 1, 1)
        Phylo.draw(tree, axes=axes)
        plt.title("Phylogenetic Tree")
        plt.savefig(tree_png_path)
        plt.close()
        print(f"Tree visualization saved to '{tree_png_path}'")
    except Exception as e:
        print(f"An error occurred during tree visualization: {e}")
        sys.exit(1)

    print("\nAnalysis finished successfully!")


def main():
    """
    Main function to parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="PhyloGene: A command-line tool to generate a phylogenetic tree from gene sequences."
    )
    parser.add_argument(
        "fasta_file",
        type=str,
        help="Path to the input multi-sequence FASTA file."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="phylogene_output",
        help="Directory to save the output files (default: phylogene_output)."
    )
    args = parser.parse_args()
    run_phylogenetic_analysis(args.fasta_file, args.output_dir)


if __name__ == "__main__":
    main()

