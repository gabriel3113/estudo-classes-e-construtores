# src/estudo_csv/csv_processor.py
from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Sequence, Union
import pandas as pd

class CsvProcessor:
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self.df: pd.DataFrame | None = None

    def carregar_csv(self) -> pd.DataFrame:
        # utf-8-sig evita BOM no Windows; parse_dates converte a coluna "data" pra datetime se existir
        self.df = pd.read_csv(self.file_path, encoding="utf-8-sig")
        # tipagens úteis
        if "data" in self.df.columns:
            self.df["data"] = pd.to_datetime(self.df["data"], errors="coerce")
        if "preço" in self.df.columns:
            # garante float (se vier string)
            self.df["preço"] = pd.to_numeric(self.df["preço"], errors="coerce")
        return self.df

    def filtrar_por(
        self,
        colunas: Sequence[str],
        atributos: Sequence[object],
        *,
        case_insensitive: bool = True,
        strip: bool = True,
        float_tol: float | None = None,
    ) -> pd.DataFrame:
        """
        Aplica múltiplos filtros em AND sobre o DataFrame carregado.
        - case_insensitive/strip: normaliza comparação de strings.
        - float_tol: tolerância para comparação de floats (ex.: 0.01).
        """
        if self.df is None:
            raise RuntimeError("Chame carregar_csv() antes de filtrar.")

        if len(colunas) != len(atributos):
            raise ValueError("Não tem o mesmo número de colunas e atributos.")

        if len(colunas) == 0:
            return self.df.copy()

        mask = pd.Series(True, index=self.df.index)
        for col, val in zip(colunas, atributos):
            if col not in self.df.columns:
                raise KeyError(f"Coluna '{col}' não existe no DataFrame.")

            series = self.df[col]

            # Comparação para strings
            if pd.api.types.is_string_dtype(series):
                s = series.astype("string")
                if strip:
                    s = s.str.strip()
                if case_insensitive and isinstance(val, str):
                    mask &= (s.str.casefold() == val.strip().casefold())
                else:
                    mask &= (s == (val.strip() if isinstance(val, str) else val))

            # Comparação para números (com tolerância opcional)
            elif pd.api.types.is_numeric_dtype(series) and isinstance(val, (int, float)):
                if float_tol is not None:
                    mask &= (series - float(val)).abs() <= float_tol
                else:
                    mask &= (series == float(val))

            # Fallback: igualdade direta
            else:
                mask &= (series == val)

        return self.df[mask].copy()
