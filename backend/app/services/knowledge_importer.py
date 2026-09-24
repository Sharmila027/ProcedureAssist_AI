import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path


class KnowledgeImporter:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="government_procedures"
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def load_dataset(self, file_path):
        return pd.read_csv(file_path)

    def create_document(self, row):
        return f"""
Service Name: {row['Service Name']}
Service Code: {row['Code']}
Department: {row['Dept']}
SLA: {row['SLA (Days)']}
CAN Required: {row['CAN Required?']}
Validity: {row['Validity']}
File Rules: {row['File Rules']}
Target Demographic: {row['Target Demographic']}
Government Fee: {row['Govt Fee']}
e-Sevai Fee: {row['e-Sevai Fee']}
Access Sources: {row['Online & Offline Access Sources']}
Tracker URL: {row['Tracker URL']}
First Appellate Authority: {row['First Appellate Authority']}
Workflow: {row['Workflow']}
"""

    def import_file(self, file_path):

        df = self.load_dataset(file_path)

        documents = []
        ids = []
        metadatas = []

        for index, row in df.iterrows():

            document = self.create_document(row)

            documents.append(document)

            ids.append(
                f"{row['Code']}_{index}"
            )

            metadatas.append({
                "service_name": str(row["Service Name"]),
                "code": str(row["Code"]),
                "department": str(row["Dept"]),
                "source": str(row["Tracker URL"])
            })

        embeddings = self.model.encode(
            documents
        ).tolist()

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            f"Imported {len(documents)} services "
            f"from {Path(file_path).name}"
        )


if __name__ == "__main__":

    importer = KnowledgeImporter()

    importer.import_file(
        "../knowledge_base/documents/dataset1.csv"
    )

    importer.import_file(
        "../knowledge_base/documents/dataset2.csv"
    )

    print("Knowledge base created successfully.")