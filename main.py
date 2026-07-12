from src.phenotype import PhenotypePredictor
from src.recommendation import DrugRecommendation
from src.report import ReportGenerator

# Create Objects
predictor = PhenotypePredictor()
recommend = DrugRecommendation()
report = ReportGenerator()

print("=" * 65)
print("          NEUROPGX TREATMENT ADVISOR")
print("=" * 65)

# User Input
patient_name = input("Enter Patient Name : ")
disease = input("Enter Disease      : ")
gene = input("Enter Gene         : ")
genotype = input("Enter Genotype     : ")

# Predict Phenotype
phenotype = predictor.predict(gene, genotype)

# Drug Recommendation
result = recommend.recommend(disease, gene, phenotype)

print("\n")
print("=" * 65)
print("          NEUROPGX TREATMENT REPORT")
print("=" * 65)

print("\nPATIENT INFORMATION")
print("-" * 65)
print(f"Patient Name        : {patient_name}")
print(f"Disease             : {disease}")

print("\nGENETIC ANALYSIS")
print("-" * 65)
print(f"Gene                : {gene}")
print(f"Genotype            : {genotype}")
print(f"Predicted Phenotype : {phenotype}")

if result is not None:

    print("\nTREATMENT RECOMMENDATION")
    print("-" * 65)

    print(f"Recommended Drug    : {result['Drug']}")
    print(f"Recommendation      : {result['Recommendation']}")
    print(f"Alternative Drug    : {result['AlternativeDrug']}")
    print(f"Clinical Reason     : {result['Reason']}")
    print(f"Evidence Level      : {result['EvidenceLevel']}")

    print("\n" + "=" * 65)
    print("         REPORT GENERATED SUCCESSFULLY")
    print("=" * 65)

    # Save Report
    report.generate(
        patient_name,
        disease,
        gene,
        genotype,
        phenotype,
        result["Drug"],
        result["Recommendation"],
        result["AlternativeDrug"],
        result["Reason"],
        result["EvidenceLevel"]
    )

else:

    print("\nNo recommendation found for the given patient information.")

print("\nThank you for using NeuroPGx Advisor!")
print("=" * 65)