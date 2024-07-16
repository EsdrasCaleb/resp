import pandas as pd

df = pd.read_csv("teste.csv")

def format_float(x):
   if abs(x) < 0.0001:
       return f"{x:.2e}"  # Scientific notation for values less than 0.0001
   else:
       return f"{x:.4f}"  # Default formatting for other values

print(df.to_latex(index=False,float_format=lambda x: format_float(x)))