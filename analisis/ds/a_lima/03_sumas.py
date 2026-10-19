# -*- coding: utf-8 -*-
"""Fusiona datos de sumas (KFG summary + ascher_sum_relationships) con la cohorte."""
import pandas as pd, numpy as np, re
BASE = r"."
sel = pd.read_csv(BASE + r"\analisis\ds\a_lima\cohorte.csv")
s = pd.read_csv(BASE + r"\data\external\data-science-khipu-article\data\khipu_summary.csv")
r = pd.read_csv(BASE + r"\data\external\data-science-khipu-article\data\ascher_sum_relations\ascher_sum_relationships.csv")
r["name"] = r["name"].str.extract(r">([A-Z0-9_]+)<")

sumcols = ["num_top_cord_sum_clusters","num_top_cord_double_sum_clusters","num_banded_clusters",
           "num_seriated_clusters","num_decreasing_clusters","num_pendant_cords","num_top_cords",
           "num_subsidiary_cords","num_s_cords","num_z_cords","recto_cords","verso_cords"]
s2 = s[["kfg_name"]+sumcols].rename(columns={"kfg_name":"kfg"})
relcols = ["num_pendant_pendant_sum","num_pendant_pendants_color_sum","num_indexed_pendant_sum",
           "num_subsidiary_pendant_sum","num_cluster_cluster_sum","num_cluster_sum_bands","num_ascher_decreasing_cluster"]
r2 = r[["name"]+relcols].rename(columns={"name":"kfg"})

M = sel[["kfg","procedencia"]].merge(s2, on="kfg", how="left").merge(r2, on="kfg", how="left")
M.to_csv(BASE + r"\analisis\ds\a_lima\sumas_quipus.csv", index=False)

print("Cobertura summary:", sel["kfg"].isin(s2["kfg"]).sum(), "/", len(sel))
print("Cobertura ascher rel:", sel["kfg"].isin(r2["kfg"]).sum(), "/", len(sel))
tot = M[relcols].sum()
print("\nSumas registradas (Ascher) en la cohorte:")
print(tot.to_string())
print("\nQuipus con >=1 relacion de suma de algun tipo:",
      (M[relcols].fillna(0).sum(axis=1)>0).sum(), "/", len(M))
# por procedencia
M["tiene_suma"] = M[relcols].fillna(0).sum(axis=1)>0
print("\nPor procedencia:")
print(M.groupby("procedencia")["tiene_suma"].agg(["sum","count"]).to_string())
print("\nTop quipus por n relaciones de suma:")
print(M.assign(n=M[relcols].fillna(0).sum(axis=1)).sort_values("n",ascending=False)[["kfg","procedencia","n"]].head(12).to_string())
