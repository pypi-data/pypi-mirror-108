# Advanced usage:

```python
from wbib import wbib
from yaml import yaml
```

## Render dashboard from an yaml configuration

First, set up an yaml file with the content of the page. 
An example file is available [here]("./advanced/config.yaml")

The structure of the yaml is like this:

```yaml
title: Advanced Wikidata Bib

subtitle: >
    Advanced mode of Wikidata Bib

restriction:
    # - Remove all options for no restriction
    #  (you can also remove this section and edit the query directly on queries.py)
    #   Categories are united by AND (i.e. will need to match both author area and institution region)
    # Qids inside categoy are united by OR(i.e. will select works that match any of the listed topics)
    author_area:
    #  - Q12149006 # Metabolomics
    topic_of_work:
    #  - Q12174 # Example: Obesity
    institution_region:
    #  - Q12585 # Example: Latin America (works for countries and beyond)
    gender:
    # - Q6581072 # Female
    event:
    #  - Q106587263 # 1st Human Cell Atlas Latin America Single Cell RNA-seqData Analysis Workshop
    author_is_topic_of:
        - Q106757464 # Science Super-Heroes: 52 Brazilians and their transformative research

sections:
    # Comment out to remove from dashboard;
    # Change the order to change the order on the dashboard
    - articles
    - map of institutions
    - list of authors
    - list of topics
    - list of journals
    - curation of author items
    - curation of author affiliations

license_statement: >
    This content is available under a 
    <a target="_blank" href="https://creativecommons.org/publicdomain/zero/1.0/"> 
    Creative Commons CC0</a> license.
    </a>
scholia_credit: >
    SPARQL queries adapted from 
    <a target="_blank" href="https://scholia.toolforge.org/">Scholia</a>
creator_credit: >
    Dashboard generated via <a target="_blank" href="https://pypi.org/project/wbib/">Wikidata Bib</a>

```

once the file is set, it can serve as an input for the render_dashboard function:

```python

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

html = wbib.render_dashboard(config, mode="advanced", filepath="dashboard.html")
```


See the results [here](./advanced/dashboard.html).