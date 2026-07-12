import pandas as pd


class PhenotypePredictor:

    def __init__(self):
        # Load genotype database
        self.data = pd.read_csv("data/genotype_database.csv")

        # Remove unwanted spaces
        self.data["Gene"] = self.data["Gene"].astype(str).str.strip()
        self.data["Genotype"] = self.data["Genotype"].astype(str).str.strip()
        self.data["Phenotype"] = self.data["Phenotype"].astype(str).str.strip()

    def predict(self, gene, genotype):

        gene = gene.strip()
        genotype = genotype.strip()

        result = self.data[
            (self.data["Gene"] == gene) &
            (self.data["Genotype"] == genotype)
        ]

        if result.empty:
            return "Phenotype Not Found"

        return result.iloc[0]["Phenotype"]