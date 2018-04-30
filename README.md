# RSV-NLP
NLP system for RSV

# Dependencies
This system runs with several dependencies including:
- Python 3.6.5
- PyRuSH 1.0.2
- pyConTextNLP 0.6.2.0
- pandas 0.22.0

An environment.yml file is provided which will provide the correct conda environment for this system.
Go here to learn how to load the environment from the yml file: https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file

# Use
Run main.py

## Inputs
Folder of documents to process 
- Each document should have an annotation file (.ann) and corresponding text file (.txt).
Regular expression based rules
- Default is to run from Documents/Example

Rules for sentence segmentation, classification targets, classification context, extraction targets, and rules to analyze words between targets during extraction.
- Should be in yml or tsv file format for all except the "between_rules" which should be a list.
- Default rules are included.

## Output
The system will output two excel files (classification.xlsx and extraction.xlsx).



