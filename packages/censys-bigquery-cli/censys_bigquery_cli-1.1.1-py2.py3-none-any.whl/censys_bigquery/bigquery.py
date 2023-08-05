"""Interact with the Censys Big Query."""
import csv
import json
import os
import time
from typing import ItemsView, Optional, Tuple, List

from google.cloud import bigquery

Results = Tuple[dict]


class CensysBigQuery:
    """Censys Big Query for CLI."""

    def __init__(
        self,
        user_filename: Optional[str] = None,
        google_application_credentials: Optional[str] = None,
    ):
        """Inits CensysBigQuery.

        Args:
            user_filename (str): Optional; Path to write output.
            google_application_credentials (str): Optional; Path of Google Application Credentials.

        Raises:
            Exception: Please set the system variable GOOGLE_APPLICATION_CREDENTIALS
        """
        self.creds = google_application_credentials or os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS", None
        )

        if not self.creds:
            raise Exception(
                "Please set the system variable GOOGLE_APPLICATION_CREDENTIALS"
            )

        self.bq_client = bigquery.Client()

        if not user_filename or user_filename == "None":
            self.output_file = "censys-bq-output-{}".format(time.time())
        else:
            self.output_file = user_filename

    def format_json_result(self, result: ItemsView) -> dict:
        """Formats result items as a dict.

        Args:
            result (ItemsView): Result items.

        Returns:
            dict: Dict of result items.
        """
        record_dict = {x[0]: x[1] for x in result}
        return record_dict

    def _write_csv_file(self, results: Results):
        """Write results to CSV file.

        Args:
            results (Results): Results from BigQuery.
        """
        output_filename = os.path.join(os.getcwd(), "{}.csv".format(self.output_file))

        with open(output_filename, "w") as csv_file:
            field_names_set = False
            writer: Optional[csv.DictWriter] = None

            for result in results:
                # During the first run, set the column headers
                formatted_result = self.format_json_result(result.items())

                if not field_names_set:
                    writer = csv.DictWriter(
                        csv_file, fieldnames=formatted_result.keys()
                    )
                    writer.writeheader()
                    field_names_set = True

                if writer:
                    writer.writerow(formatted_result)

        print(
            "Wrote approximately {} bytes to file {}".format(
                os.path.getsize(output_filename), output_filename
            )
        )

    def _write_json_file(self, results: Results):
        """Write results to JSON file.

        Args:
            results (Results): Results from BigQuery.
        """
        output_filename = os.path.join(os.getcwd(), "{}.json".format(self.output_file))

        with open(output_filename, "w") as json_file:
            for row in results:
                data = json.dumps(self.format_json_result(row.items()))
                json_file.write(data)

        print(
            "Wrote approximately {} bytes to file {}".format(
                os.path.getsize(output_filename), output_filename
            )
        )

    def _write_results(self, results: Results, output_type: List[str] = ["screen"]):
        """Write results.

        Args:
            results (Results): Results from BigQuery.
            output_type (str): Optional; Output type. Defaults to "screen".
        """
        if "screen" in output_type:
            for row in results:
                print(json.dumps(self.format_json_result(row.items())))
        elif "json" in output_type:
            self._write_json_file(results)
        elif "csv" in output_type:
            self._write_csv_file(results)

    def query_censys(self, query: str, output_type: List[str] = ["screen"]) -> Results:
        """Query Censys BigQuery.

        Args:
            query (str): Query string.
            output_type (str): Optional; Output type. Defaults to "screen".

        Returns:
            Results: Results from BigQuery.
        """
        client = self.bq_client

        query_job = client.query("{}".format(query))
        results = query_job.result()  # Waits for job to complete.

        self._write_results(results=results, output_type=output_type)

        return results
