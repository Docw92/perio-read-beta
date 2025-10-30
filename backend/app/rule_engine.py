{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # rule_engine.py\
from typing import List, Dict, Any\
\
# Numeric mappings (simple, transparent)\
POCKET_MAP = [\
    (1, 1, 3),\
    (4, 2, 6),\
    (7, 3, 9),\
    (10, 4, 999)\
]\
\
RECESSION_CLASS_MAP = \{\
    "I": 2,\
    "II": 2,\
    "III": 3,\
    "IV": 4\
\}\
\
FURCATION_MAP = \{\
    0: 0,\
    1: 3,\
    2: 2,\
    3: 3,\
    4: 4\
\}\
\
MOBILITY_MAP = \{\
    0: 0,\
    1: 4,\
    2: 2,\
    3: 3\
\}\
\
COMPOSITE_RANGES = [\
    (0.0, 1.0, "Excellent"),\
    (1.1, 2.0, "Mild"),\
    (2.1, 3.0, "Moderate"),\
    (3.1, 4.0, "Severe")\
]\
\
def pocket_numeric(pd_mm: float) -> int:\
    for low, numeric, high in POCKET_MAP:\
        if low <= pd_mm <= high:\
            return numeric\
    if pd_mm >= 10:\
        return 4\
    return 1\
\
def recession_numeric(recession_class: str) -> int:\
    if not recession_class:\
        return 0\
    return RECESSION_CLASS_MAP.get(recession_class, 0)\
\
def furcation_numeric(fclass: int) -> int:\
    return FURCATION_MAP.get(fclass, 0)\
\
def mobility_numeric(mob: int) -> int:\
    return MOBILITY_MAP.get(mob, 0)\
\
def compute_tooth_score(param: Dict[str, Any]) -> Dict[str, Any]:\
    scores = []\
    pd = float(param.get("pocket_depth_mm", 0))\
    pnum = pocket_numeric(pd)\
    scores.append(pnum)\
\
    rclass = param.get("recession_class", None)\
    rnum = recession_numeric(rclass) if rclass else 0\
    if rnum:\
        scores.append(rnum)\
\
    mob = int(param.get("mobility_grade", 0))\
    mnum = mobility_numeric(mob)\
    if mnum:\
        scores.append(mnum)\
\
    fclass = int(param.get("furcation_class", 0))\
    fnum = furcation_numeric(fclass)\
    if fnum:\
        scores.append(fnum)\
\
    if param.get("bleeding_on_probing", False):\
        scores.append(2)\
\
    if not scores:\
        composite = 0.0\
    else:\
        composite = sum(scores) / len(scores)\
        composite = round(composite, 2)\
\
    label = "Unknown"\
    for low, high, name in COMPOSITE_RANGES:\
        if low <= composite <= high:\
            label = name\
            break\
\
    return \{\
        "tooth_number": param.get("tooth_number"),\
        "component_scores": scores,\
        "composite_score": composite,\
        "severity_label": label\
    \}\
\
def fuse_patient_scores(tooth_scores: List[Dict[str, Any]]) -> Dict[str, Any]:\
    composites = [t["composite_score"] for t in tooth_scores if t["composite_score"] > 0]\
    if not composites:\
        overall = 0.0\
    else:\
        overall = round(sum(composites) / len(composites), 2)\
\
    overall_label = "Unknown"\
    for low, high, name in COMPOSITE_RANGES:\
        if low <= overall <= high:\
            overall_label = name\
            break\
    return \{"overall_score": overall, "overall_label": overall_label\}\
\
def treatment_decision_for_tooth(tooth_score: Dict[str, Any], param: Dict[str, Any]) -> str:\
    composite = tooth_score.get("composite_score", 0)\
    mobility = int(param.get("mobility_grade", 0))\
    furc = int(param.get("furcation_class", 0))\
    if composite >= 3.5 or mobility >= 3 or furc >= 3:\
        return "Consider extraction / advanced prosthetic option (refer to decision chart)"\
    if composite >= 2.5:\
        return "Advanced periodontal therapy (possible surgery), evaluate prognosis"\
    return "Conservative therapy (scaling, root planing, maintenance)"\
\
def analyze_patient(patient_dict: Dict[str, Any]) -> Dict[str, Any]:\
    clinical_list = patient_dict.get("clinical_params", [])\
    tooth_results = []\
    for param in clinical_list:\
        tr = compute_tooth_score(param)\
        decision = treatment_decision_for_tooth(tr, param)\
        tr["treatment_recommendation"] = decision\
        tooth_results.append(tr)\
    fused = fuse_patient_scores(tooth_results)\
    return \{\
        "patient_id": patient_dict.get("patient_id"),\
        "tooth_results": tooth_results,\
        "fused": fused\
    \}\
}