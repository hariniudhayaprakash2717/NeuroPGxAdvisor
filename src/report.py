class ReportGenerator:

    def generate(self, patient_name, disease, gene, genotype,
                 phenotype, drug, recommendation,
                 alternative_drug, reason, evidence):

        filename = f"reports/{patient_name}_Report.txt"

        with open(filename, "w") as file:

            file.write("========================================\n")
            file.write("      NeuroPGx Treatment Report\n")
            file.write("========================================\n\n")

            file.write(f"Patient Name : {patient_name}\n")
            file.write(f"Disease      : {disease}\n")
            file.write(f"Gene         : {gene}\n")
            file.write(f"Genotype     : {genotype}\n")
            file.write(f"Phenotype    : {phenotype}\n\n")

            file.write("Drug Recommendation\n")
            file.write("---------------------------\n")

            file.write(f"Drug               : {drug}\n")
            file.write(f"Recommendation     : {recommendation}\n")
            file.write(f"Alternative Drug   : {alternative_drug}\n")
            file.write(f"Reason             : {reason}\n")
            file.write(f"Evidence Level     : {evidence}\n")

        print("\nReport Saved Successfully!")
        print("Location :", filename)