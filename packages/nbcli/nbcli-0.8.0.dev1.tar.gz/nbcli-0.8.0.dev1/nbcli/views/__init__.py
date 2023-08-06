"""Load views used by nbprint."""

from nbcli.views.tools import BaseView                          # noqa: F401
from nbcli.views.device import DcimDevicesView                  # noqa: F401
from nbcli.views.interfaces import DcimInterfacesView           # noqa: F401
from nbcli.views.racks import DcimRacksView, DcimRUsView        # noqa: F401
from nbcli.views.locations import DcimLocationsView             # noqa: F401
from nbcli.views.sites import DcimSitesView                     # noqa: F401
from nbcli.views.aggregates import IpamAggregatesView           # noqa: F401
from nbcli.views.ip_addresses import IpamIpAddressesView        # noqa: F401
from nbcli.views.object_changes import ExtrasObjectChangesView  # noqa: F401
