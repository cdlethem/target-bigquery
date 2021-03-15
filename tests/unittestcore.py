import json
import os
import sys
import unittest

from google.cloud import bigquery


class BaseUnitTest(unittest.TestCase):

    def setUp(self):
        os.environ["TARGET_BIGQUERY_STATE_FILE"] = "state.json.tmp"
        self.delete_temp_state()

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "sandbox", "sa.json"))

        self.client = None
        self.project_id = None
        self.dataset_id = None

    def tearDown(self):
        self.delete_temp_state()
        self.delete_dataset()

    def set_cli_args(self, ds_delete=True, *args, **kwargs):
        arg = [arg for arg in args]
        for k, v in kwargs.items():
            if k == "stdin":
                sys.stdin = open(v, "r")
                continue

            arg.append("--{}".format(k))
            arg.append("{}".format(v))

        sys.argv[1:] = arg

        if "config" in kwargs and ds_delete:
            c = None
            with open(kwargs["config"], "r") as f:
                c = json.load(f)

            self.project_id = c["project_id"]
            self.dataset_id = c["dataset_id"]
            self.client = bigquery.Client(project=self.project_id)

            self.delete_dataset()

    def delete_temp_state(self):
        try:
            os.remove(os.environ["TARGET_BIGQUERY_STATE_FILE"])
        except:
            pass

    def delete_dataset(self):
        try:
            self.client.delete_dataset(
                dataset=self.dataset_id,
                delete_contents=True
            )
        except:
            pass

    def get_state(self):
        state = []
        with open(os.environ["TARGET_BIGQUERY_STATE_FILE"], "rb") as f:
            for line in f:
                state.append(json.loads(line))

        return state
