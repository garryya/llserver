import flask

report_view = flask.Blueprint('report', __name__)


@report_view.route('/get_full', methods=['GET'])
def get_full_report():
    """
    Return a report describing the behavior of a file under analysis in a sandboxed execution.

    URL: /report/get_full
    GET parameters:

    - uuid: identifier of the report. In this example implementation,
      this is used to identify the base report file that needs to be
      parsed to produce the response. This file is found at data/reports/<UUID>.json

    The response is not the raw json found on the file system, but a smaller JSON dictionary
    that contains only the following fields

    - score: integer 0-100 (from top level field `score` of raw report)
    - malicious_activity: list of activity strings (from top level field `malicious_activity` of raw report)
    - file_writes: list of distinct filenames that were written to during analysis. This comes from the `filename`
      fields of all the elements in all of the `file_writes` nodes of the raw report JSON.
    - file_reads: list of distinct filenames that were read from during analysis. This comes from the `filename`
      fields of all the elements in all of the `file_reads` nodes of the raw report JSON.

    Errors:

    This method is allowed to all users with the PERMISSION_VIEW_FULL_REPORT permissions.
    Otherwise, return an HTTP 403 error.

    If the uuid is not found, return an HTTP 422 error.
    """
    return "TODO: Implement full report"


@report_view.route('/get', methods=['GET'])
def get_report():
    """
    Return a report.

    URL: /report/get

    This method is the same as get_full_report, with the following differences:

    - Users with only PERMISSION_VIEW_REPORT are allowed to use this method, but not get_full_report().

    - the file_reads and file_writes lists in this report are filtered to only return file names for which
      the raw report included an `iostatus` value of `FILE_OPENED` or `FILE_CREATED`. E.g., in the snippet of
      file_writes below, the `\Device\Afd\Endpoint" would not be included in the response
      of this method, while "C:\Windows\SysWOW64\zhq.dll" would be.

        {
            iostatus: [
                "FILE_SUPERSEDED"
            ],
            filename: "\Device\Afd\Endpoint"
        },
        {
            abs_path: "C:\Windows\SysWOW64\zhq.dll",
            filename: "C:\Windows\SysWOW64\zhq.dll",
            iostatus: [
                "FILE_OPENED",
                "FILE_OVERWRITTEN",
            ],
            accesses: ...
            file_attributes: ...
        }

    """
    return "TODO: Implement report"




