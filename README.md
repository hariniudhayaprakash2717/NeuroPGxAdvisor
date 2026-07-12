# NeuroPGx Advisor

## Project Title

NeuroPGx Advisor: A Pharmacogenomics Treatment Recommendation Tool for Neurological Disorders

---

## Description

NeuroPGx Advisor is a Python-based application that provides personalized drug recommendations for neurological disorders based on a patient's genetic profile.

The system predicts the patient's phenotype from genotype information and recommends suitable medications using pharmacogenomics guidelines.

---

## Objectives

- Predict phenotype using genotype information.
- Recommend appropriate drugs based on pharmacogenomics.
- Reduce adverse drug reactions.
- Support personalized medicine.
- Generate a patient treatment report.

---

## Features

- Patient Information Input
- Phenotype Prediction
- Drug Recommendation
- Alternative Drug Suggestion
- Clinical Reason Display
- Evidence Level Display
- Automatic Report Generation

---

## Technologies Used

- Python 3
- Pandas
- CSV Database
- VS Code

---

## Project Structure

```
NeuroPGxAdvisor/
│
├── data/
│   ├── disease_database.csv
│   ├── drug_database.csv
│   ├── gene_information.csv
│   ├── genotype_database.csv
│   └── sample_patients.csv
│
├── src/
│   ├── database.py
│   ├── phenotype.py
│   ├── recommendation.py
│   ├── report.py
│
├── reports/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Database Files

### disease_database.csv

Contains neurological diseases and related genes.

### genotype_database.csv

Maps genotype to phenotype.

### drug_database.csv

Contains pharmacogenomic drug recommendations.

### gene_information.csv

Stores information about important pharmacogenomic genes.

### sample_patients.csv

Contains sample patient records for testing.

---

## Workflow

1. User enters patient details.
2. Software predicts phenotype.
3. Drug recommendation is generated.
4. Alternative drug is suggested.
5. Treatment report is generated.

---

## How to Run

Install the required library:

```
pip install pandas
```

Run the project:

```
python main.py
```

---

## Sample Output

```
Patient Name : Harini

Disease : Depression

Gene : CYP2D6

Genotype : *4/*4

Phenotype : Poor Metabolizer

Drug : Fluoxetine

Recommendation : Avoid

Alternative Drug : Escitalopram

Evidence Level : High
```

---

## Future Enhancements

- Graphical User Interface (GUI)
- PDF Report Generation
- Integration with PharmGKB and CPIC databases
- Web Application Deployment
- Machine Learning-based Drug Prediction

---

## Author

Muthu Murugan

B.E. Electronics and Communication Engineering

Undergraduate Student

---

## License

This project is developed for academic and educational purposes.