\# FortyGuard Product Evaluation



\## Overview

A practical evaluation of the FortyGuard Temperature Dashboard and API.



\## Evaluation Areas

\- Temperature Classification Map (TCM)

\- Time of Measure

\- Exceedance

\- Persistence

\- API response inspection

\- Heatmap visualization



\## Technologies

\- Python

\- Requests

\- JSON

\- FortyGuard API



\## Scripts

\- test\_heatmap.py: Submits heatmap requests.

\- check\_status.py: Retrieves analysis results.

\- inspect\_exceedance.py: Inspects exceedance results.

\- inspect\_persistence.py: Inspects persistence results.

\- inspect\_time\_measure.py: Inspects time-of-measure results.

\- compare\_time\_results.py: Compares time-of-measure tests.

\- visualize\_heatmap.py: Generates a heatmap visualization.



\## Results

All four tested analytical types were successfully submitted and their completed results retrieved.



This evaluation tests product functionality. It does not independently validate temperature accuracy.



\## Security

The API key is supplied through the FORTYGUARD\_API\_KEY environment variable. No API credentials should be committed to this repository.

