# miscset.io


"""File and other stream i/o methods.

Writing to

- **text files**
- **stderr**

or reading from

- **text files** as lines
- **yaml** or **json** files as dictionaries
- **csv** files as array

or parsing data (dictionary, json/yaml) to and from a ``Parsable`` class object made easy!
"""


import os
import sys
import json
import yaml
import logging


logger = logging.getLogger()


def write(text, path):
    """Write text to a file.

    A file at a path is opened writable,
    and the text from a string variable is inserted.

    Args:
        text (str): Text to write to a file at `path`.
        path (str): File path.
    """
    fs = open(path, "w")
    fs.write(text)
    fs.close()
    return


def write_stderr(text):
    """Write text to standard error of the console.

    A text string is written to the system standard error stream.

    Args:
        text (str): A text to write to stderr.
    """
    sys.stderr.write(text)
    sys.stderr.flush()
    return


def read_lines(path, mode = "r"):
    """Read text as lines from a file.

    A file is read line by line and parsed as a list of string.

    Args:
        path (str): File path.
        mode (str): File mode for `open`.

    Returns:
        list: Lines read from the file as a list of strings.
    """
    fs = open(path, mode)
    lines = fs.readlines()
    fs.close()
    lines = [line.rstrip(os.linesep) for line in lines]
    return lines


def read_yaml(path):
    """Read a YAML file.

    Read a YAML formatted file into a dictionary object.
    Supports logging (see :py:mod:`miscset`).

    Args:
        path (str): File path.

    Returns:
        dict: Content of a YAML file parsed as dictionary.
    """
    d = {}
    if not os.path.isfile(path):
        logging.error("missing YAML file at {}".format(path))
        return d
    with open(path, "r") as fs:
        try:
            logging.info("parsing YAML from file {}".format(path))
            d = yaml.safe_load(fs)
        except yaml.YAMLError as e:
            logging.error("failed importing {} YAML {}".format(path, e))
    logging.debug("parsed YAML content as {}".format(d))
    return d


def read_json(path):
    """Read a JSON file.

    Read a JSON formatted file into a dictionary object.

    Args:
        path (str): File path to JSON formatted file.

    Returns:
        dict: Content of a JSON file parsed as dictionary.
    """
    fs = open(path, "r")
    d = json.load(fs)
    fs.close()
    return d


def read_csv(path, sep = ","):
    """Read a CSV file.

    Read a separated value file into an array of
    fields per line.

    Args:
        path (str): File path.
        sep (str): A field separator, such as ","

    Returns:
        list: A list of fields per line.
    """
    csv = []
    lines = read_lines(path)
    for line in lines:
        fields = line.split(sep)
        csv.append(fields)
    return csv


class Parsable(object):
    """A class where slots are parsable.

    Provides methods to import and export values for data slots from dictionaries.
    """

    def __init__(self):
        """Initialize a Parsable object.

        Initializes the object and calls the `reset` function.
        """
        self.reset()

    def reset(self):
        """Reset slots to default values.

        This method implemented here does not affect anything.

        It is a placeholder for subclasses implementing this method.
        When calling the class constructor, this method will be called.
        """
        return

    def __str__(self):
        """Create a string representation of the object data slots."""
        return self.description()

    def get_text(self, name = None, sep = os.linesep + "  ", private = True):
        """Return a description.

        Args:
            name (str): Provide a custom name of the class shown as prefix.
            sep (str): A string separating the values.
            private (bool): Show privat slots (starting with an underscore "_").

        Returns:
            str: A text representation of the object data slots.
        """
        if name is None:
            name = "miscset.io.Parsable"
        txt = "<{}:".format(name)
        for var in vars(self):
            if not private and var.startswith("_"):
                continue
            value = getattr(self, var)
            if type(value) == type([]):
                value = [ str(i) for i in value ]
            if type(value) == type({}):
                value = { k: str(v) for k,v in value.items() }
            txt += "{}{}={}".format(sep, var, value)
        txt += ">"
        return txt

    def get_dict(self):
        """Return values of the data slots as dictionary.

        Same as accessing the `__dict__` slot from a class instance.

        Returns:
            dict: A dictionary with keys named as the class instance slots
                containing the respective values.
        """
        return self.__dict__

    def get_json(self):
        """"Return values of the data slots as a json string.

        Returns:
            str: A JSON formatted string.
        """
        return json.dumps(self.get_dict())

    def get_yaml(self):
        """"Return values of the data slots as a yaml string.

        Returns:
            str: A YAML formatted string.
        """
        return yaml.dump(self.get_dict())

    def import_dict(self, obj, add = False):
        """Import a dictionary into data slots.

        Args:
            obj (dict): A dictionary from which keys become
               slots and assigned the values.
            add (bool): Whether to add a key as slot if it
               did not yet exist.
        """
        self.reset()
        if not type(obj) == type({}):
            return
        if obj is None:
            return
        if not callable(getattr(obj, "keys", None)):
            return
        varnames = [key for key, value in vars(self).items()]
        #obj = { key: obj.get(key) for key in obj.keys() if key in varnames }
        for key, value in obj.items():
            if key not in varnames and not add:
                continue
            setattr(self, key, value)

