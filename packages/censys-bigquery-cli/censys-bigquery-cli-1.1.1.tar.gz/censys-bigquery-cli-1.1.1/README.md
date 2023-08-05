# Censys BigQuery Command Line Tool

[![PyPI](https://img.shields.io/pypi/v/censys-bigquery-cli?color=orange&logo=pypi&logoColor=orange)](https://pypi.org/project/censys-bigquery-cli/)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue?logo=python)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-organge.svg?logo=git&logoColor=organge)](http://makeapullrequest.com)
[![License](https://img.shields.io/github/license/censys/censys-bigquery?logo=apache)](https://github.com/censys/censys-bigquery/blob/main/LICENSE)

This script allows users to query the data in Censys Data BigQuery Project from the command line. The results from the query can be exported as JSON, CSV, or viewed from the terminal screen.

> Note: the Censys Data BigQuery Project is available to enterprise customers and approved academic researchers. For more information on product tiers, contact sales@censys.io.

## Setting Up a Service Account in BigQuery

Prior to using the BiqQuery Command Line Tool, you'll need to set up a service account that is associated with your Google Cloud Platform.

Google provides documentation on how to create a service account, either via the GCP Console or the Command Line. Visit [Getting started with authentication](https://cloud.google.com/docs/authentication/getting-started) for full documentation.

Be sure to set the `GOOGLE_APPLICATION_CREDENTIALS` environmental variable.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```

## Install

The library can be installed using `pip`.

```bash
pip install censys-bigquery-cli
```

OR

```bash
pip install git+https://github.com/censys/censys-bigquery
```

## Usage

The script allows you to input SQL queries as arguments in the script, returning the results as screen output (default), JSON, or CSV.

Here are some example queries:

```bash
censys_bq 'SELECT ip, ports, protocols, tags FROM `censys-io.ipv4_public.current` WHERE location.city = "Ann Arbor" and REGEXP_CONTAINS(TO_JSON_STRING(tags), r"rsa-export") LIMIT 25'
```

```bash
censys_bq 'with user_ports as (
SELECT [443, 3306, 6379] as selected_ports
)

SELECT DISTINCT ip, TO_JSON_STRING(user_ports.selected_ports)
  FROM `censys-io.ipv4_banners_public.current`, user_ports, UNNEST(services) as s
  WHERE (SELECT LOGICAL_AND(a_i IN (SELECT port_number FROM UNNEST(services))) FROM UNNEST(user_ports.selected_ports) a_i) LIMIT 15' --format csv
```

```bash
censys_bq 'SELECT COUNT(ip), p80.http.get.body_sha256
FROM `censys-io.ipv4_public.current`
WHERE REGEXP_CONTAINS(p80.http.get.body, r"(?i)coinhive.min.js>")
GROUP BY p80.http.get.body_sha256
ORDER BY 1 DESC' --format json
```

```bash
censys_bq 'with Data as (SELECT
  distinct fingerprint_sha256
FROM
  `censys-io.certificates_public.certificates`, UNNEST(parsed.subject.organization) as po, UNNEST(parsed.names) as parsed_names
WHERE
   REGEXP_CONTAINS(TO_JSON_STRING(parsed.names), r"[.]example[.]")
)

SELECT
  distinct ip
FROM
  `censys-io.ipv4_banners_public.current` as c, UNNEST(services)
      JOIN Data as d on d.fingerprint_sha256 = certificate.fingerprints.sha256
LIMIT 20' --format json
```

## Resources

- [Source](https://github.com/censys/censys-bigquery)
- [Issue Tracker](https://github.com/censys/censys-bigquery/issues)
- [Censys Homepage](https://censys.io/)

## Contributing

All contributions (no matter how small) are always welcome.

## Development

```bash
git clone git@github.com:censys/censys-bigquery.git
cd censys-bigquery/
pip install -e ".[dev]"
```

## License

This software is licensed under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

- Copyright (C) 2021 Censys, Inc.
