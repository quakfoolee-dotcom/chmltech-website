Chmltech Online Journal, Vol. 106, Issue 17 - OEE dataset and LLM test set
data/shifts.csv, data/stops.csv, data/skus.csv : four-week extract of the composite three-line bottling plant
oee_appendix.py     : reference OEE calculator (python3 oee_appendix.py)
oee_reference.py    : (needs numpy; overwrites data and answers) rebuilds the data, reference results, the eight-error study (results.json) and questions.json
questions.json      : 24 questions with reference answers and tolerances
grade.py            : python3 grade.py answers.json   (answers as {"Q01": 77.7, "Q20": "L2", ...})
