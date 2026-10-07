"""Which Phoenix surface answers which question.

Agents reach Phoenix data two ways: one REST tool per endpoint, and a read-only
analytics SQL pair. Left to the tool list alone they over-reach for SQL on
single-entity lookups and page through REST results to count. The text here is
the one statement of the rule, shown in the server instructions, on the SQL and
``execute`` tools, and in PXI's tool instructions.
"""

SQL_WHEN = (
    "Use SQL when the answer is computed over many traces, spans, sessions, runs, or "
    "examples at once: a count, sum, average, percentile, ratio, distribution, ranking, "
    "group-by, time window, or a join across spans, traces, sessions, datasets, "
    "experiments, or costs. Do not page through REST results and aggregate them in code; "
    "one statement does it."
)

REST_WHEN = (
    "Use the REST tool for a resource when the question identifies one thing and wants "
    "its fields or what hangs off it, even as a count or a list: a trace, span, session, "
    "project, dataset, example, experiment, run, prompt, evaluator, annotation, or setting "
    "named by id, by name, or by position such as the latest or the first. The REST "
    "object is the resolved view, with templates, output configs, statuses, and formatted "
    "errors that the tables hold as raw JSON or not at all."
)

# The lookup tool for each resource, so a client need not search for it.
REST_LOOKUP_TOOLS = (
    "project: `getProject(project_identifier)`, `getProjects(name_contains)`. trace: "
    "`getSpans(project_identifier, trace_id)` for its spans; "
    "`listProjectTraces(project_identifier, filter, session_identifier)` for the traces of a "
    "project. span: `getSpans(project_identifier, span_id | parent_id | name | status_code)`. "
    "session: `getSession(session_identifier)`, `listProjectSessions(project_identifier)`. "
    "annotations: `listSpanAnnotationsBySpanIds`, `listTraceAnnotationsByTraceIds`, "
    "`listSessionAnnotationsBySessionIds` (project_identifier plus the ids); configs: "
    "`listAnnotationConfigs`, `getProjectAnnotationConfigs(project_identifier)`. dataset: "
    "`listDatasets(name)`, `getDataset(id)`, `getDatasetExamples(id, version_id, split)`, "
    "`listDatasetVersionsByDatasetId(id)`, `listDatasetSplits`, "
    "`listDatasetLabelsForDataset`. experiment: `listExperiments(dataset_id)`, "
    "`getExperiment(experiment_id)`, `listExperimentRuns(experiment_id)`, "
    "`getExperimentJSON(experiment_id)` for runs with their evaluations. prompt: "
    "`getPrompts`, `listPromptVersions(prompt_identifier)`, "
    "`getPromptVersionLatest(prompt_identifier)`, "
    "`getPromptVersionByTagName(prompt_identifier, tag_name)`. models and providers: "
    "`getModelProviders`, `getCustomModelProviders`. users: `getUsers`, `getViewer`."
)

_DESCRIPTION = (
    "Phoenix data is reachable two ways: one REST tool per resource, and read-only analytics "
    "SQL. Pick by the shape of the answer, not by which tool is nearest. First ask whether the "
    "question names one entity; if it does, start from that resource's REST tool."
)
_ORDER = (
    "Decide the surface before reading a schema: `describeSqlSchema` is for writing SQL, not "
    "for finding out what Phoenix stores, and a question about one named entity does not need "
    "it."
)

_REST_CALL = (
    "Call them with `execute` as `await call_tool(name, params)`; `get_schema` shows the "
    "parameters, and `search` finds the rest."
)

DATA_ACCESS_INSTRUCTIONS = f"""<phoenix_data_access>
  <description>{_DESCRIPTION}</description>
  <rest>{REST_WHEN}</rest>
  <rest_tools>{REST_LOOKUP_TOOLS} {_REST_CALL}</rest_tools>
  <sql>{SQL_WHEN} The tools are `describeSqlSchema` and `executeSql`.</sql>
  <order>{_ORDER}</order>
</phoenix_data_access>"""

EXECUTE_SQL_DESCRIPTION = f"""Run one read-only SQL statement over the allowlisted Phoenix tables.

{REST_WHEN} {SQL_WHEN}

A statement may be at most 2 KiB of UTF-8; split longer work. The result holds
`columns`, `rows`, `row_count_is_partial` (the authoritative truncation flag),
`applied`, and `notes`, or an `error` envelope when the SQL is refused: check for
`error` before reading `rows`. Preserve any error in your summary. `estimated_rows`
is available only on PostgreSQL and is a planner estimate, not a count. Code-mode
`call_tool` returns the envelope as a dictionary, so do not `json.loads` it. With
`validate_only=True` the statement is checked but returns no rows."""

DESCRIBE_SQL_SCHEMA_DESCRIPTION = (
    "Return the allowlisted analytics SQL schema for telemetry, datasets, experiments, "
    "evaluators, and prompts, for writing `executeSql` statements. Call it once a question "
    "needs SQL (an answer computed across many rows); for the fields of one identified "
    "entity, call that resource's REST tool instead."
)

EXECUTE_ROUTING_NOTE = (
    "For one identified trace, span, session, project, dataset, experiment, or prompt, call "
    "its REST tool (`getSpans`, `getSession`, `getProject`, `getDataset`, `getExperiment`, "
    "`getPromptVersionLatest`, and the others the server instructions list); choose "
    "`executeSql` only for answers computed over many of them at once."
)

__all__ = [
    "DATA_ACCESS_INSTRUCTIONS",
    "DESCRIBE_SQL_SCHEMA_DESCRIPTION",
    "EXECUTE_ROUTING_NOTE",
    "EXECUTE_SQL_DESCRIPTION",
    "REST_LOOKUP_TOOLS",
    "REST_WHEN",
    "SQL_WHEN",
]
