#!/bin/bash

python3 scc-stats.py --equivalences cleaned_equivalence_classes.txt --format aggregate > interveners-aggregate-2009-2018.tsv
python3 scc-stats.py --equivalences cleaned_equivalence_classes.txt --format individual > interveners-individual-2009-2018.tsv
python3 scc-stats.py --equivalences cleaned_equivalence_classes.txt --format pollen > interveners.pollen
