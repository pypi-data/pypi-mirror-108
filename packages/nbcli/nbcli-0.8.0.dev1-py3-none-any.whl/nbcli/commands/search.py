"""Search sub command to emulate Netbox main search bar."""


from pynetbox.core.query import Request
from pynetbox.core.endpoint import response_loader
from nbcli.commands.base import BaseSubCommand
from nbcli.core.utils import app_model_by_loc
from nbcli.views.tools import nbprint


class SearchSubCommand(BaseSubCommand):
    """Search Netbox objects with the given searchterm.

    The List of search objects can be modified in:
    $CONF_DIR/user_config.yml
    """

    name = 'search'
    parser_kwargs = dict(help='Search Netbox Objects')

    def setup(self):
        """Add parser arguments to search sub command."""
        self.parser.add_argument('obj_type',
                                 type=str,
                                 nargs='?',
                                 help='Object type to search')

        self.parser.add_argument('searchterm',
                                 help='Search term')

    def run(self):
        """Run a search of Netbox objects and show a table view of results.

        Usage Examples:

        - Search all object types for 'server1':
          $ nbcli search server1

        - Search the interface object type for 'eth 1':
          $ nbcli search interface 'eth 1'
        """
        if hasattr(self.netbox.nbcli.conf, 'nbcli') and \
                ('search_objects' in self.netbox.nbcli.conf.nbcli.keys()):
            self.search_objects = self.netbox.nbcli.conf.nbcli['search_objects']
        else:
            self.search_objects = ['provider',
                                  'circuit',
                                  'site',
                                  'rack',
                                  'location',
                                  'device_type',
                                  'device',
                                  'virtual_chassis',
                                  'cable',
                                  'power_feed',
                                  'vrf',
                                  'aggregate',
                                  'prefix',
                                  'address',
                                  'vlan',
                                  'secret',
                                  'tenant',
                                  'cluster',
                                  'virtual_machine']

        def search(ep):
            req = Request(filters=dict(q=self.args.searchterm),
                          base=ep.url,
                          token=ep.token,
                          session_key=ep.session_key,
                          http_session=ep.api.http_session)

            rep = req._make_call(add_params=dict(limit=15))

            result = list()

            if rep.get('results'):
                result = response_loader(rep['results'], ep.return_obj, ep)

            return result

        self.nbprint = nbprint

        if self.args.obj_type:
            modellist = [self.args.obj_type]
        else:
            modellist = self.search_objects

        result_count = 0

        print('')
        for obj_type in modellist:
            model = app_model_by_loc(self.netbox, obj_type)
            result = search(model)
            full_count = model.count(self.args.searchterm)
            if len(result) > 0:
                result_count += 1
                print('{}\n{}'.format(obj_type.title(), '=' * len(obj_type)))
                self.nbprint(result)
                if len(result) < full_count:
                    print('*** See all {} results: '.format(full_count) +
                          "'$ nbcli filter {} {}' ***".
                          format(obj_type, self.args.searchterm))
                print('')
        if result_count == 0:
            self.logger.warning('No results found')
            print('')
