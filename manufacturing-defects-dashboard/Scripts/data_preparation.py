import pandas as pd
import numpy as np

df = pd.read_csv("defects_data.csv")

# ── 1. Fecha ──────────────────────────────────────────
df['defect_date'] = pd.to_datetime(df['defect_date'])
df['Year']        = df['defect_date'].dt.year
df['Month']       = df['defect_date'].dt.month
df['Month_Name']  = df['defect_date'].dt.strftime('%B')
df['Quarter']     = df['defect_date'].dt.quarter.apply(lambda x: f'Q{x}')
df['Week']        = df['defect_date'].dt.isocalendar().week.astype(int)
df['Day_of_Week'] = df['defect_date'].dt.day_name()

# ── 2. Severity ordenada ──────────────────────────────
severity_order = {'Minor': 1, 'Moderate': 2, 'Critical': 3}
df['Severity_Rank'] = df['severity'].map(severity_order)

# ── 3. Rangos de costo ────────────────────────────────
df['Cost_Range'] = pd.cut(
    df['repair_cost'],
    bins=[0, 250, 500, 750, 1000],
    labels=['$0-250', '$251-500', '$501-750', '$751-1000']
)

# ── 4. Flag de defecto crítico ────────────────────────
df['Is_Critical'] = (df['severity'] == 'Critical').astype(int)

# ── 5. Costo acumulado por producto ───────────────────
df['Cumulative_Cost_per_Product'] = df.groupby('product_id')['repair_cost'].cumsum()

# ── 6. Validación ─────────────────────────────────────
print(f"✅ Dataset limpio: {len(df):,} registros")
print(f"   Rango de fechas : {df['defect_date'].min().date()} → {df['defect_date'].max().date()}")
print(f"   Defect types    : {df['defect_type'].value_counts().to_dict()}")
print(f"   Severity dist.  : {df['severity'].value_counts().to_dict()}")
print(f"   Repair cost     : min ${df['repair_cost'].min():.2f} | avg ${df['repair_cost'].mean():.2f} | max ${df['repair_cost'].max():.2f}")
print(f"   Critical defects: {df['Is_Critical'].sum()} ({df['Is_Critical'].mean()*100:.1f}%)")

# ── 7. Exportar para Power BI ─────────────────────────
df.to_csv("manufacturing_defects_clean.csv", index=False)
print(f"\n✅ Archivo exportado: manufacturing_defects_clean.csv")