# This file was ported from GStreamer cebero project
# url:  https://gitlab.freedesktop.org/gstreamer/cerbero/errors.py
#  
# ------------------------------------------------------------
# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


from gettext import gettext as _


class ConanXException(Exception):
    header = ''
    msg = ''

    def __init__(self, msg=''):
        self.msg = msg
        Exception.__init__(self, self.header + msg)


class ConfigurationError(ConanXException):
    header = 'Configuration Error: '


class UsageError(ConanXException):
    header = 'Usage Error: '


class FatalError(ConanXException):
    header = 'Fatal Error: '
    def __init__(self, msg='', arch=''):
        self.arch = arch
        ConanXException.__init__(self, msg)

class CommandError(ConanXException):
    header = 'Command Error: '
    def __init__(self, msg, cmd, returncode):
        msg = 'Running {!r} returned {}\n{}'.format(cmd, returncode, msg or '')
        FatalError.__init__(self, msg)


class BuildStepError(ConanXException):
    recipe = ''
    step = ''

    def __init__(self, recipe, step, trace='', arch=''):
        self.recipe = recipe
        self.step = step
        self.arch = arch
        ConanXException.__init__(self, _("Recipe '%s' failed at the build "
            "step '%s'\n%s") % (recipe, step, trace))


class RecipeNotFoundError(ConanXException):

    def __init__(self, recipe):
        ConanXException.__init__(self, _("Recipe '%s' not found") % recipe)


class PackageNotFoundError(ConanXException):

    def __init__(self, package):
        ConanXException.__init__(self, _("Package '%s' not found") % package)


class EmptyPackageError(ConanXException):

    def __init__(self, package):
        ConanXException.__init__(self, _("Package '%s' is empty") % package)


class MissingPackageFilesError(ConanXException):

    def __init__(self, files):
        ConanXException.__init__(self, _("The following files required by "
            "this package are missing:\n %s") % '\n'.join(files))


class InvalidRecipeError(ConanXException):

    def __init__(self, recipe, message=''):
        ConanXException.__init__(self,
                _("Recipe %s is invalid:\n%s") % (recipe, message))


class AbortedError(Exception):
    pass
