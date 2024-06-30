import pandas as pd
from transformers import pipeline

# Define the file paths for the input CSV files
file1 = 'sistematicreviens/player_centered_game_desigC.csv'
output_file = 'sistematicreviens/player_centered_game_desigC2.csv'
# Read the CSV files into pandas dataframes
df1 = pd.read_csv(file1)

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
#df1['Abstract'].fillna('', inplace=True)
df1['Abstract'] = df1['Abstract'].fillna('')
labels = ["Player Centered Design"]

def classify_abstract(abstract):
    if abstract.strip() == '':
        return 0.0
    result = classifier(abstract, candidate_labels=labels)
    return result['scores'][0]  # The label with the highest score

df1['Player Centered Design Score (Title)']  = df1['Title'].apply(classify_abstract)
df1['Player Centered Design Score']  = df1['Abstract'].apply(classify_abstract)
df1.to_csv(output_file, index=False)

print(f"Data has been successfully written to {output_file}")