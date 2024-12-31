from textwrap import dedent


class FcloudError:
    """A class from which all classes containing error data are inherited"""

    example_error = (
        "Error title",
        "Error message. Some info about error and maybe link to docs",
    )

    unknown_error = (
        "Unknown error",
        dedent("""\
        Details: {}
        """),
    )
