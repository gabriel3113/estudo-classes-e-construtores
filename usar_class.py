from csv_teste import CsvProcessor

proc = CsvProcessor("exemplo.csv")
proc.carregar_csv()

# Filtrar por estado e preço
resultado = proc.filtrar_por(["estado", "preço"], ["SP", 378.02])

print(resultado)
