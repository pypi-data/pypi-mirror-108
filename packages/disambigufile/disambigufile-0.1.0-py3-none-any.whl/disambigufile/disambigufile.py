# Class with file-like interface to a file found in provided search path

import logging
import os
import re

import attr

from .exceptions import *

@attr.s(auto_attribs=True)
class Disambigufile:
    '''
    Examples
    --------

    ::

        from disambigufile import Disambigufile
        import disambigufile.exceptions

        path = '/bin:/usr/bin:/usr/local/bin'
        try:
            print(Disambigufile('^ls', path=path))
        except disambigufile.exceptions.Error as e:
            print(f"unable to disambiguate file; exception: {e}")

        path = 'path1:path2'
        try:
            with Disambigufile(r'^asdf', path=path).open() as f:
                print(f.read())
        except disambigufile.exceptions.Error as e:
            print(f"unable to disambiguate file; exception: {e}")

        # search for unique file matching ~/Datasets/*2019-08-19*/data*
        path='~/Datasets'
        try:
            hit = Disambigufile(
                pattern='2019-08-19',
                path=path,
                dir=True,
                subpattern='^data',
            )
            print(hit)
        except disambigufile.exceptions.Error as e:
            print(f"unable to disambiguate file; exception: {e}")

    Attributes
    ----------

    pattern : str
        regular expression describing desired match
    dir : bool (default: False)
        whether top level match should consider directories
    expand : bool (default: True)
        expand ~ and environment variables in path components
    path : str (default: None)
        directories to search (: separated)
    subpattern : str (default: None)
        regular expression describing file pattern match
        for when dir = True, what to look for inside directories
    '''
    pattern: str
    dir: bool = False
    expand: bool = True
    path: str = None
    subpattern: str = None

    def __attrs_post_init__(self):
        self.pathlist = re.split(r':', self.path)
        # strip out trailing slashes
        self.pathlist = map(lambda x: x.rstrip('/'), self.pathlist)
        self.pathlist = self._expandpath(self.pathlist)

        # all the action occurs in the _search() method
        self._search()
        if len(self.found) == 0:
            raise NoMatchError
        if len(self.found) > 1:
            raise AmbiguousMatchError(self.found)
        # if no exceptions, there will be an unambiguous match
        # use hit() or open() to interact with the item found

    def _expandstr(self, x):
        'expand ~ and then expand environment variables'
        if self.expand:
            logging.debug(f"expanding {x}")
            return(os.path.expandvars(os.path.expanduser(x)))
        else:
            return(x)

    def _expandpath(self, pathlist):
        'expand elements of path'
        return(list(map(lambda x: self._expandstr(x), pathlist)))

    def _search_path_for_file(self, pattern, pathlist):
        'return list of files matching pattern in a path'
        # filter out missing directories
        pathlist = filter(lambda x: os.path.isdir(x), pathlist)
        files = []
        for dir in pathlist:
            for file in os.listdir(dir):
                if re.search(pattern, file):
                    files.append(f"{dir}/{file}")
        return(files)

    def _search(self):
        'search path for matching files'

        logging.debug(f"considering {self.pathlist}")
        # search for matches with each element of path
        found = self._search_path_for_file(self.pattern, self.pathlist)

        if self.dir:
            # if unambiguous, found will be a single-item list
            # however, dir = True might have multiple matches & 1 sub-match
            # example, pattern = asdf, subpattern = data
            # if asdf1/data and asdf2 both exist, asdf1/data is unique
            newfound = []
            for x in found:
                if os.path.isdir(x):
                    submatches = filter(
                        lambda x: re.search(self.subpattern, x),
                        os.listdir(x),
                    )
                    for submatch in submatches:
                        newfound.append(f"{x}/{submatch}")
                else:
                    newfound.append(x)
            found = newfound

        self.found = found

    def hit(self):
        'return filename of disambiguated file'
        return(self.found[0])

    def open(self, mode='r'):
        'open disambiguated file and return file-like object'
        return(open(self.found[0], mode))

    def __str__(self):
        return(self.hit())

