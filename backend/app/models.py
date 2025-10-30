{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # models.py\
from pydantic import BaseModel\
from typing import Optional, List\
\
class ClinicalParam(BaseModel):\
    tooth_number: int\
    pocket_depth_mm: float\
    gingival_recession_mm: float\
    recession_class: Optional[str] = None   # I,II,III,IV\
    mobility_grade: Optional[int] = 0\
    furcation_class: Optional[int] = 0\
    bleeding_on_probing: Optional[bool] = False\
\
class Patient(BaseModel):\
    patient_id: Optional[str] = None\
    name: Optional[str] = None\
    age: Optional[int] = None\
    sex: Optional[str] = None\
    medical_history: Optional[dict] = \{\}\
    clinical_params: List[ClinicalParam] = []\
}