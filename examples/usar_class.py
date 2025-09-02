# examples/usar_class.py
from pathlib import Path
from estudo_csv.csv_processor import CsvProcessor

ROOT = Path(__file__).resolve().parents[1]
csv_path = ROOT / "data" / "exemplo.csv"

proc = CsvProcessor(csv_path)
df = proc.carregar_csv()

# Filtrar por estado e preço 378.02 com tolerância de 1 centavo
resultado = proc.filtrar_por(
    ["estado", "preço"],
    ["SP", 378.02],
    float_tol=0.01  # evita falhas por precisão de ponto flutuante
)

print(resultado)
