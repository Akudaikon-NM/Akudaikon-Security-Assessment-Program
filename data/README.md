# Data Directory

## Critical Files

### `veris_to_cis_lookup.csv`
**Purpose:** VERIS threat taxonomy to CIS Controls mapping table  
**Status:** Production-ready, version-controlled  
**Rows:** 71 mappings  
**Last Updated:** December 26, 2025

**Integration Chain:**
```
Controls (controls.py)
  ↓ VERIS Fields
veris_to_cis_lookup.csv (71 mappings)
  ↓ CIS Controls
CIS_TO_MITRE_TACTICS (Streamlit app)
  ↓ ATT&CK Tactics
YAML Control Framework
  ↓ Board Narratives
```

**Schema:**
- `veris_field` (string): VERIS taxonomy field in dot notation
- `cis_control` (float): CIS Control number (1.0-18.0)

**Cardinality:** Many-to-many  
**Most Comprehensive VERIS Field:** `action.hacking.variety.Exploit vuln` → 10 CIS Controls  
**Most Versatile CIS Control:** CIS 4 (Secure Configuration) → 7 VERIS fields

**Maintenance:**
- Review frequency: Annually or upon CIS Controls version update
- Approval authority: CISO, Threat Intelligence Lead
- Documentation: `docs/THREAT_TAXONOMY_ENRICHMENT.yaml`

## Excluded Directories

The following directories are excluded via `.gitignore` to prevent version control bloat:

- `data/raw/` - Raw datasets (not curated reference data)
- `datasets/` - Bulk analytical datasets
- Generated files: `*.parquet`, `*.xlsx`, `*.pkl`

## Data Governance

**Regulatory Anchor:** 12 CFR § 748.0 (Security Program)  
**Purpose:** Support threat taxonomy enrichment for Board-ready cyber risk narratives  
**Classification:** Internal Use Only (no member data, no credentials)
