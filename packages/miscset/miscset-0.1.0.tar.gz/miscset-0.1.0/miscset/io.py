# miscset.io


"""File and other stream i/o methods."""


import os
import sys
import json
import yaml
import logging


logger = logging.getLogger()


def write(text, path):
    """Write text to a file.
    
    Args:
        text (string): Text to write to a file at `path`.
        path (string): File path.
    """
    fs = open(path, "w")
    fs.write(text)
    fs.close()
    return


def write_stderr(text):
    """Write text to standard error of the console.

    Args:
        text (string): A text to write to stderr.
    """
    sys.stderr.write(text)
    sys.stderr.flush()
    return


def read_lines(path, mode = "r"):
    """Read text as lines from a file.
    
    Args:
        path (string): File path.
        mode (string): File mode for `open`.

    Returns:
        (list of string): Lines read from the file.
    """
    fs = open(path, mode)
    lines = fs.readlines()
    fs.close()
    lines = [line.rstrip("\n") for line in lines]
    return lines


def read_yaml(path):
    """Read a yaml file and return a dictionary.
    
    Args:
        path (string): File path.

    Returns:
        (dict): Content of a YAML file parsed as dictionary.
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
    """Read a JSON formatted file

    Args:
        path (string): File path to JSON formatted file.
    
    Returns:
        (dict): Content of a JSON file parsed as dictionary.
    """
    fs = open(path, "r")
    d = json.load(fs)
    fs.close()
    return d


def read_csv(path, sep = ","):
    """Read a separated value file into an array.
    
    Args:
        path (string): File path.
        sep (string): A field separator, such as ","
    
    Returns:
        (list of lists): A list of fields per line.
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
        """Return a description
        
        Args:
            name (string): Provide a custom name of the class shown as prefix.
            sep (string): A string separating the values.
            private (boolean): Show privat slots (starting with an underscore "_").
        
        Returns:
            (string): A text representation of the object data slots.
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
        """Return values of the data slots as dictionary."""
        return self.__dict__

    def get_json(self):
        """"Return values of the data slots as a json string.

        Returns:
            (string): A JSON formatted string.
        """
        return json.dumps(self.get_dict())

    def get_yaml(self):
        """"Return values of the data slots as a yaml string.

        Returns:
            (string): A YAML formatted string.
        """
        return yaml.dump(self.get_dict())

    def import_dict(self, obj, add = False):
        """Import a dictionary into data slots.

        Args:
            obj (dict): A dictionary from which keys become
               slots and assigned the values.
            add (boolean): Whether to add a key as slot if it
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
