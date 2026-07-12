import pandas as pd


class DrugRecommendation:

    def __init__(self):
        # Load drug database
        self.data = pd.read_csv("data/drug_database.csv")

        # Remove unwanted spaces
        self.data["Disease"] = self.data["Disease"].astype(str).str.strip()
        self.data["Gene"] = self.data["Gene"].astype(str).str.strip()
        self.data["Phenotype"] = self.data["Phenotype"].astype(str).str.strip()

    def recommend(self, disease, gene, phenotype):

        disease = disease.strip()
        gene = gene.strip()
        phenotype = phenotype.strip()

        # Search matching disease, gene and phenotype
        result = self.data[
            (self.data["Disease"] == disease) &
            (self.data["Gene"] == gene) &
            (self.data["Phenotype"] == phenotype)
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()