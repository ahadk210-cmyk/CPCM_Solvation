import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("cpcm_results.csv")

# Derived columns
df["Gap_gas_eV"] = df["LUMO_gas_eV"] - df["HOMO_gas_eV"]
df["Gap_cpcm_eV"] = df["LUMO_cpcm_eV"] - df["HOMO_cpcm_eV"]
df["Gap_change_pct"] = (df["Gap_cpcm_eV"] - df["Gap_gas_eV"]) / df["Gap_gas_eV"] * 100
df["Dipole_change_pct"] = (df["Dipole_cpcm_D"] - df["Dipole_gas_D"]) / df["Dipole_gas_D"] * 100

# ---- Plot 1: HOMO-LUMO gap, gas vs water ----
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(df))
width = 0.35
ax.bar(x - width/2, df["Gap_gas_eV"], width, label="Gas-phase", color="#4C72B0")
ax.bar(x + width/2, df["Gap_cpcm_eV"], width, label="CPCM(Water)", color="#55A868")
ax.set_xticks(x)
ax.set_xticklabels(df["Molecule"], rotation=20, ha="right")
ax.set_ylabel("HOMO-LUMO Gap (eV)")
ax.set_title("HOMO-LUMO Gap: Gas-Phase vs. Aqueous (CPCM)")
ax.legend()
plt.tight_layout()
plt.savefig("../Outputs/gap_comparison.png", dpi=200)
plt.close()

# ---- Plot 2: % change in gap (highlights direction) ----
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#C44E52" if v > 0 else "#55A868" for v in df["Gap_change_pct"]]
ax.bar(df["Molecule"], df["Gap_change_pct"], color=colors)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("HOMO-LUMO Gap Change (%)")
ax.set_title("Solvent-Induced Shift in HOMO-LUMO Gap")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("../Outputs/gap_change_percent.png", dpi=200)
plt.close()

# ---- Plot 3: Dipole moment, gas vs water ----
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width/2, df["Dipole_gas_D"], width, label="Gas-phase", color="#4C72B0")
ax.bar(x + width/2, df["Dipole_cpcm_D"], width, label="CPCM(Water)", color="#55A868")
ax.set_xticks(x)
ax.set_xticklabels(df["Molecule"], rotation=20, ha="right")
ax.set_ylabel("Dipole Moment (Debye)")
ax.set_title("Dipole Moment: Gas-Phase vs. Aqueous (CPCM)")
ax.legend()
plt.tight_layout()
plt.savefig("../Outputs/dipole_comparison.png", dpi=200)
plt.close()

# ---- Plot 4: Solvation free energy ----
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(df["Molecule"], df["Gsolv_kcal_mol"], color="#8172B2")
ax.set_ylabel("ΔG(solv) (kcal/mol)")
ax.set_title("Solvation Free Energy (Water)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("../Outputs/gsolv_comparison.png", dpi=200)
plt.close()

# ---- Print summary table ----
summary = df[["Molecule", "Gap_gas_eV", "Gap_cpcm_eV", "Gap_change_pct",
              "Dipole_gas_D", "Dipole_cpcm_D", "Gsolv_kcal_mol"]]
summary.to_csv("solvation_summary_table.csv", index=False)
print(summary.to_string(index=False))
print("\nAll 4 plots saved to ../Outputs/")
