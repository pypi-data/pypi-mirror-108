import json
import pandas as pd
from company_name_matching.matching_function import DefaultMatching

json.load(open("company_name_matching/abbreviations.json"))
pd.read_csv("company_name_matching/elf_company.csv")