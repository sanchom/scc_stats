This script gets the list of appeals for a given calendar year, then
checks the docket for the list of interveners in each case. It prints
a markdown-formatted output summarizing this info. The output, when
rendered, looks like this:

# 2018
|Total decisions|Decisions with interventions|Appeals as of right|Appeals as of right with interventions|
|---------------|----------------------------|-------------------|--------------------------------------|
| 59 | 39 (66.10%) | 18 | 3 (16.67%) |

|Neutral citation|Case name|From|Criminal?|As of right?|Interveners|Dockets|
|----------------|---------|----|---------|------------|-----------|-------|
| 2018 SCC 1 | [R. v. Seipp](https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/16957/index.do) | British Columbia | criminal |  | 1 |  [[1]](https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas=37513) |
| 2018 SCC 2 | [Delta Air Lines Inc. v. Lukács](https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/16958/index.do) | Federal Court of Appeal |  |  | 4 |  [[1]](https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas=37276) |
| 2018 SCC 3 | [Quebec (Commission des normes, de l’équité, de la santé et de la sécurité du travail) v. Caron](https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/16959/index.do) | Quebec |  |  | 8 |  [[1]](https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas=36605) |
| 2018 SCC 4 | [Williams Lake Indian Band v. Canada (Aboriginal Affairs and Northern Development)](https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/16969/index.do) | Federal Court of Appeal |  |  | 8 |  [[1]](https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas=36983) |
| 2018 SCC 5 | [R. v. Canadian Broadcasting Corp.](https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/16981/index.do) | Alberta | criminal |  | 2 |  [[1]](https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas=37360) |

The `.pkl` file is a cache of info already downloaded from the SCC,
but if you want to retrieve fresh data, just delete the `.pkl` file.

The Dockerfile provides an environment that you can run this all in.
