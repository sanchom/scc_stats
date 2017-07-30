# interveners.rkt

This script gets the list of appeals for a given calendar year, then
checks the docket for the list of interveners in each case. It prints
a tab-separated list of docket numbers, case names, and intervener
names, if any.

For example:

```
36792	Shane Rayshawn Vassell v. Her Majesty the Queen
36068	Barrett Richard Jordan v. Her Majesty the Queen	Attorney General of Alberta
36068	Barrett Richard Jordan v. Her Majesty the Queen	Criminal Lawyers' Association (Ontario)
36068	Barrett Richard Jordan v. Her Majesty the Queen	British Columbia Civil Liberties Association
36112	Her Majesty the Queen v. Kenneth Gavin Williamson	Attorney General of Alberta
36112	Her Majesty the Queen v. Kenneth Gavin Williamson	British Columbia Civil Liberties Association
36112	Her Majesty the Queen v. Kenneth Gavin Williamson	Criminal Lawyers' Association (Ontario)
```