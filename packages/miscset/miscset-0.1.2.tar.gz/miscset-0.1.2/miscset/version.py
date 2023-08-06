# miscset.version

"""Version variables.

The package version stored in python variables.
Following a semantic versioning, the package version is stored as tuple (`version_` variable)
and for convenience concatenated to a string variable (`version_string_`).
"""

version_ = (0, 1, 2, "")
"""The (semantic) version of the module implemented as tuple with major, minor, bugfix and alpha/beta version."""

version_string_ = "{}.{}.{}{}".format(*version_)
"""The (semantic) version of the module concatenated to a string."""

