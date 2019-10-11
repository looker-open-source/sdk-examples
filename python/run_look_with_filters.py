import json
import sys
from typing import cast, Dict, List, Union

from looker_sdk import client, models

sdk = client.setup("../looker.ini")


def main():
    """Given a look id, obtain the query behind it and run it with the desired
     filter values.
    """
    look_id = sys.argv[1] if len(sys.argv) > 1 else ""
    filter_args = iter(sys.argv[2:])
    filter_values: List[Dict[str, str]] = []

    if not (look_id and len(sys.argv[2:]) > 0 and len(sys.argv[2:]) % 2 == 0):
        print(
            "Please provide: <lookId> <filter_1> <filter_value_1> "
            "<filter_2> <filter_value_2> ..."
        )
        return

    for filter_name in filter_args:
        filter_value = next(filter_args)
        filter_values.append({filter_name: filter_value})

    query = get_look_query(int(look_id))
    for filters in filter_values:
        results = run_query_with_filter(query, filters)
        print(f"Query results with filters={filters}:\n{results}", end="\n\n")


def get_look_query(id: int) -> models.Query:
    """Returns the query associated with a given look id.
    """
    look = sdk.look(id)
    query = look.query
    assert isinstance(query, models.Query)
    return query


TJson = List[Dict[str, Union[str, int, float, bool, None]]]


def run_query_with_filter(query: models.Query, filters: Dict[str, str]) -> TJson:
    """Runs the specified query with the specified filters.
    """
    request = create_query_request(query, filters)
    json_ = sdk.run_inline_query("json", request, cache=False)
    json_resp = cast(TJson, json.loads(json_))
    return json_resp


def create_query_request(q: models.Query, filters: Dict[str, str]) -> models.WriteQuery:
    return models.WriteQuery(
        model=q.model,
        view=q.view,
        fields=q.fields,
        pivots=q.pivots,
        fill_fields=q.fill_fields,
        filters=filters,
        sorts=q.sorts,
        limit=q.limit,
        column_limit=q.column_limit,
        total=q.total,
        row_total=q.row_total,
        subtotals=q.subtotals,
        dynamic_fields=q.dynamic_fields,
        query_timezone=q.query_timezone,
    )


main()
