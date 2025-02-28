# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from datetime import datetime

from airflow.api_connexion.schemas.task_schema import TaskCollection, task_collection_schema, task_schema
from airflow.operators.empty import EmptyOperator


class TestTaskSchema:
    def test_serialize(self):
        op = EmptyOperator(
            task_id="task_id",
            start_date=datetime(2020, 6, 16),
            end_date=datetime(2020, 6, 26),
        )
        result = task_schema.dump(op)
        expected = {
            "class_ref": {
                "module_path": "airflow.operators.empty",
                "class_name": "EmptyOperator",
            },
            "depends_on_past": False,
            "downstream_task_ids": [],
            "end_date": "2020-06-26T00:00:00+00:00",
            "execution_timeout": None,
            "extra_links": [],
            "owner": "airflow",
            "operator_name": "EmptyOperator",
            "params": {},
            "pool": "default_pool",
            "pool_slots": 1.0,
            "priority_weight": 1.0,
            "queue": "default",
            "retries": 0.0,
            "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 300, "microseconds": 0},
            "retry_exponential_backoff": False,
            "start_date": "2020-06-16T00:00:00+00:00",
            "task_id": "task_id",
            "task_display_name": "task_id",
            "template_fields": [],
            "trigger_rule": "all_success",
            "ui_color": "#e8f7e4",
            "ui_fgcolor": "#000",
            "wait_for_downstream": False,
            "weight_rule": "downstream",
            "is_mapped": False,
            "doc_md": None,
        }
        assert expected == result


class TestTaskCollectionSchema:
    def test_serialize(self):
        tasks = [EmptyOperator(task_id="task_id1", params={"foo": "bar"})]
        collection = TaskCollection(tasks, 1)
        result = task_collection_schema.dump(collection)
        expected = {
            "tasks": [
                {
                    "class_ref": {
                        "class_name": "EmptyOperator",
                        "module_path": "airflow.operators.empty",
                    },
                    "depends_on_past": False,
                    "downstream_task_ids": [],
                    "end_date": None,
                    "execution_timeout": None,
                    "extra_links": [],
                    "operator_name": "EmptyOperator",
                    "owner": "airflow",
                    "params": {
                        "foo": {
                            "__class": "airflow.sdk.definitions.param.Param",
                            "value": "bar",
                            "description": None,
                            "schema": {},
                        }
                    },
                    "pool": "default_pool",
                    "pool_slots": 1.0,
                    "priority_weight": 1.0,
                    "queue": "default",
                    "retries": 0.0,
                    "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 300, "microseconds": 0},
                    "retry_exponential_backoff": False,
                    "start_date": None,
                    "task_id": "task_id1",
                    "task_display_name": "task_id1",
                    "template_fields": [],
                    "trigger_rule": "all_success",
                    "ui_color": "#e8f7e4",
                    "ui_fgcolor": "#000",
                    "wait_for_downstream": False,
                    "weight_rule": "downstream",
                    "is_mapped": False,
                    "doc_md": None,
                }
            ],
            "total_entries": 1,
        }
        assert expected == result
