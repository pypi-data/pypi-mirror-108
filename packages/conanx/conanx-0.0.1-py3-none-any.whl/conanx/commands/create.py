
from conanx.commands import Command, register_command, ArgparseArgument


class Create(Command):
    """
    Builds a binary package and storage in local cache.

    """

    name = 'create'
    help = 'Builds a binary package for the project and cache it in local.'
    prog = 'epm [-p PROFILE] [-s SCHEME] [-r RUNNER] %s' % name

    def __init__(self):
            args = [

                ArgparseArgument("--storage", default=None,
                                    help="all conan package will be download and cached under project directory"
                                         "that is conan storage path will be set at .conan folder in project."),

                ArgparseArgument("--clear", default=False, action="store_true",
                                    help="clear local cache of .conan in project"),

                ArgparseArgument("--archive", default=None, help="archive the package to specified path"),
                ArgparseArgument("--with-deps", dest="with_deps", default=False, action='store_true',
                                 help="archive the dependent packages, this option vaild on --archive set."),
                
                ArgparseArgument("--program", default=None, type=str, 
                                    help="this option only use for test/debug program. if the program specifed"
                                         "only run building of pargram (which in program.location), the package"
                                         "creatation should be done. if --program disable all program will not"
                                         "be build"),
                

            ]
            Command.__init__(self, args)

    def run(self, conan, args):
        print('create', args)


register_command(Create)
