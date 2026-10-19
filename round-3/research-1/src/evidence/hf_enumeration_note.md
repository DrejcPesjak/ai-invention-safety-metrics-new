# HuggingFace Hub enumeration — coverage note

Script: `scan_hf.py`. Terms searched (11): abliterated, gabliterated, MPOA,
orthogonal-reflection-bounded, heretic, Derestricted, uncensored, norm-preserving,
biprojected, Josiefied, obliterated — each under two sort orders (downloads, lastModified),
limit 200, GGUF/MLX/quantised repo ids filtered out, then `safetensors.total <= 4.2e9`
resolved per repo.

Result: **325 distinct candidate repos enumerated, 79 confirmed <= 4.2 B**
(`hf_sub4b_candidates.json`).

**Coverage caveat (reported in the dossier):** 5 of the 22 (term x sort) enumerations were
rate-limited by the Hub API and returned nothing — the terms `abliterated`, `gabliterated`,
`MPOA`, `orthogonal-reflection-bounded`, `heretic` and (partially) `Derestricted` each lost at
least one of their two sort passes. Those terms were therefore additionally covered by direct
per-term `curl` queries and by per-repo lookups; the shortlist in the dossier is
individually verified. The 79-row list is a **lower bound, not a census**.
