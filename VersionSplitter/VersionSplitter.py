from autopkglib import Processor  # noqa: F401

__all__ = ["VersionSplitter"]


class VersionSplitter(Processor):  # pylint: disable=invalid-name
    """This processor splits version numbers and returns the specified index.
    By default, it splits using a space, and returns the first item. Default
    behavior example: "3.0.8 :074a131:" --> "3.0.8".
    More examples (with "split_on" in parentheses and "index" in brackets):
    - "8.3.1.1 (154179)" --> (" ")[0] -->"8.3.1.1"
    - "1.3.1-stable" --> ("-")[0] -->"1.3.1"
    - "macosx_64bit_3.0" --> ("_")[2] -->"3.0"
    """

    input_variables = {
        "version": {
            "required": True,
            "description": "The version string that needs splitting.",
        },
        "split_on": {
            "required": False,
            "description": "The character(s) to use for splitting the "
            "version. (Defaults to a space.)",
        },
        "index": {
            "required": False,
            "description": "The index of the version string to be "
            "returned. (Defaults to 0.)",
        },
    }
    output_variables = {"version": {"description": "The cleaned up version string."}}
    description = __doc__

    def main(self):
        """Main process."""

        split_on = self.env.get("split_on", " ")
        index = self.env.get("index", 0)
        version_string = self.env["version"].split(split_on)[index]
        version_parts = version_string.split(".")
        while len(version_parts) < 4:
            version_parts.append("0")
        self.env["version"] = ".".join(version_parts)
        self.output("Split version: {}".format(self.env["version"]))


if __name__ == "__main__":
    PROCESSOR = VersionSplitter()
    PROCESSOR.execute_shell()
