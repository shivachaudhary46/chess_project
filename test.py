import pandas as pd

df = pd.read_csv("chess_project.csv")
df.to_excel("chess_project.xlsx")