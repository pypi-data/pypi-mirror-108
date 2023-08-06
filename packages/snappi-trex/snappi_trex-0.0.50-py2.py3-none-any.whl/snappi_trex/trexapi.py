import json
import snappi


class Api(snappi.Api):
    """IxNetwork implementation of the abstract-open-traffic-generator package

    Args
    ----
    - address (str): The address of the IxNetwork API Server
    - port (str): The rest port of the IxNetwork API Server
    - username (str): The username for Linux IxNetwork API Server
        This is not required when connecting to single session environments
    - password (str): The password for Linux IxNetwork API Server
        This is not required when connecting to single session environments
    """
    def __init__(self,
                 host=None,
                 username='admin',
                 password='admin',
                 license_servers=[],
                 log_level='info'):
        """Create a session
        - address (str): The ip address of the TestPlatform to connect to
        where test sessions will be created or connected to.
        - port (str): The rest port of the TestPlatform to connect to.
        - username (str): The username to be used for authentication
        - password (str): The password to be used for authentication
        """
        super(Api, self).__init__(
            host='https://127.0.0.1:11009' if host is None else host
        )
        

    def _get_addr_port(self, host):
        items = host.split('/')
        items = items[-1].split(':')

        addr = items[0]
        if len(items) == 2:
            return addr, items[-1]
        else:
            if host.startswith('https'):
                return addr, '443'
            else:
                return addr, '80'

    @property
    def snappi_config(self):
        return self._config

    def get_config_object(self, name):
        try:
            return self._config_objects[name]
        except KeyError:
            raise NameError("snappi object named {0} not found"
                            .format(name))

    def get_device_encap(self, name):
        try:
            return self._device_encap[name]
        except KeyError:
            raise NameError("snappi object named {0} not found"
                            .format(name))

    @property
    def ixn_objects(self):
        """A dict of all model unique names to ixn hrefs
        """
        return self._ixn_objects

    def get_ixn_object(self, name):
        """Returns an ixnetwork_restpy object given a unique configuration name
        """
        href = self.get_ixn_href(name)
        return self._assistant.Session.GetObjectFromHref(href)

    def get_ixn_href(self, name):
        """Returns an href given a unique configuration name
        """
        return self._ixn_objects[name]

    @property
    def assistant(self):
        return self._assistant

    def _dict_to_obj(self, source):
        """Returns an object given a dict
        """
        

    def _request_detail(self):
        """"""

    def set_config(self, config):
        """Set or update the configuration
        """
        print('setconfig')


    def set_transmit_state(self, payload):
        """Set the transmit state of flows
        """
        

    def set_link_state(self, link_state):
        """"""
    
    def set_capture_state(self, payload):
        """Starts capture on all ports that have capture enabled.
        """
        

    def get_capture(self, request):
        """Gets capture file and returns it as a byte stream
        """
        

    def get_metrics(self, request):
        """
        Gets port, flow and protocol metrics.

        Args
        ----
        - request (Union[MetricsRequest, str]): A request for Port, Flow and
          protocol metrics.
          The request content MUST be vase on the OpenAPI model,
          #/components/schemas/Result.MetricsRequest
          See the docs/openapi.yaml document for all model details
        """
        

    def add_error(self, error):
        """Add an error to the global errors
        """
        if isinstance(error, str) is False:
            self._errors.append('%s %s' % (type(error), str(error)))
        else:
            self._errors.append(error)

    def parse_location_info(self, location):
        """It will return (chassis,card,port)
        set card as 0 where that is not applicable"""
        
    
    def special_char(self, names):
        is_names = True
        if not isinstance(names, list):
            is_names = False
            names = [names]
        
        ret_list = []
        for name in names:
            if name is None:
                ret_list.append(name)
            else:
                ret_list.append(
                    name.replace('(', '\\(').replace(')', '\\)')
                        .replace('[', '\\[').replace(']', '\\]')
                        .replace('.', '\\.').replace('*', '\\*')
                        .replace('+', '\\+').replace('?', '\\?')
                        .replace('{', '\\{').replace('}', '\\}')
                )
        if is_names is True:
            return ret_list
        else:
            return ret_list[0]
    
    def _connect(self):
        """Connect to an IxNetwork API Server.
        """
        

    def _ixn_version_check(self):
        major, minor = self._globals.BuildNumber.split('.')[0:2]
        if int(major) < 9:
            return False
        if int(major) == 9 and int(minor) < 10:
            return False
        return True
    
    def _backup_errors(self):
        app_errors = self._globals.AppErrors.find()
        if len(app_errors) > 0:
            self._ixn_errors = app_errors[0].Error.find()

    def _validate_instance(self, config):
        """Validate current IxNetwork instance:
        1. Stop everything if local config is None
        2. Otherwise add warning message """
        traffic_state = self._traffic.State
        if self.snappi_config is None:
            if traffic_state == 'started':
                self._traffic_item.find()
                if len(self._traffic_item) > 0:
                    self._traffic_item.StopStatelessTrafficBlocking()
            glob_topo = self._globals.Topology.refresh()
            if glob_topo.Status  == 'started':
                self._ixnetwork.StopAllProtocols('sync')
        else:
            if traffic_state == 'started':
                msg = "Flows are in running state. " \
                      "Please stop those using set_transmit_state"
                self.add_error(msg)
                self.warning(msg)
        return config

    def _apply_change(self):
        """Apply on the fly only applicable for Device object"""
        glob_topo = self._globals.Topology.refresh()
        if glob_topo.ApplyOnTheFlyState == 'allowed':
            url = '%s/globals/topology/operations/applyonthefly' % self._ixnetwork.href
            payload = {'arg1': glob_topo.href}
            # todo: Sometime it redirect to some unknown loaction
            try:
                self._request('POST', url, payload)
            except Exception:
                pass
        
    def _request(self, method, url, payload=None):
        """"""

    def _remove(self, ixn_obj, items):
        """Remove any ixnetwork objects that are not found in the items list.
        If the items list does not exist remove everything.
        """
        valid_names = [item.name for item in items
                       if item.name is not None]
        invalid_names = []
        for item in ixn_obj.find():
            if item.Name not in valid_names:
                invalid_names.append(item.Name)
        if len(invalid_names) > 0:
            if ixn_obj._SDM_NAME == 'trafficItem':
                # can't remove traffic items that are started
                start_states = [
                    'txStopWatchExpected', 'locked', 'started',
                    'startedWaitingForStats', 'startedWaitingForStreams',
                    'stoppedWaitingForStats'
                ]
                for item in ixn_obj.find(Name='^(%s)$' %
                                         '|'.join(self.special_char(invalid_names))):
                    if item.State in start_states:
                        item.StopStatelessTraffic()
                if len(ixn_obj) > 0:
                    poll = True
                    while poll:
                        poll = False
                        for v in self.select_traffic_items().values():
                            if v['state'] not in [
                                    'error', 'stopped', 'unapplied'
                            ]:
                                poll = True
            ixn_obj.find(Name='^(%s)$' % '|'.join(self.special_char(invalid_names)))
            if len(ixn_obj) > 0:
                ixn_obj.remove()

    def _get_topology_name(self, port_name):
        return 'Topology %s' % port_name

    def select_card_aggregation(self, location):
        (hostname, cardid, portid) = location.split(';')
        payload = {
            'selects': [{
                'from':
                '/availableHardware',
                'properties': [],
                'children': [{
                    'child':
                    'chassis',
                    'properties': [],
                    'filters': [{
                        'property': 'hostname',
                        'regex': '^%s$' % hostname
                    }]
                }, {
                    'child':
                    'card',
                    'properties': ['*'],
                    'filters': [{
                        'property': 'cardId',
                        'regex': '^%s$' % abs(int(cardid))
                    }]
                }, {
                    'child':
                    'aggregation',
                    'properties': ['*'],
                    'filters': []
                }],
                'inlines': []
            }]
        }
        url = '%s/operations/select?xpath=true' % self._ixnetwork.href
        results = self._ixnetwork._connection._execute(url, payload)
        return results[0]['chassis'][0]['card'][0]

    def select_chassis_card(self, vport):
        pieces = vport['connectionStatus'].split(';')
        payload = {
            'selects': [{
                'from':
                '/availableHardware',
                'properties': [],
                'children': [{
                    'child':
                    'chassis',
                    'properties': [],
                    'filters': [{
                        'property': 'hostname',
                        'regex': '^%s$' % pieces[0]
                    }]
                }, {
                    'child':
                    'card',
                    'properties': ['*'],
                    'filters': [{
                        'property': 'cardId',
                        'regex': '^%s$' % int(pieces[1])
                    }]
                }],
                'inlines': []
            }]
        }
        url = '%s/operations/select?xpath=true' % self._ixnetwork.href
        results = self._ixnetwork._connection._execute(url, payload)
        return results[0]['chassis'][0]['card'][0]

    def select_vports(self, port_name_filters=[]):
        """Select all vports.
        Return them in a dict keyed by vport name.
        """
        payload = {
            'selects': [{
                'from':
                '/',
                'properties': [],
                'children': [{
                    'child':
                    'vport',
                    'properties': [
                        'name', 'type', 'location', 'connectionState',
                        'connectionStatus', 'assignedTo', 'connectedTo'
                    ],
                    'filters': port_name_filters
                }, {
                    'child': 'l1Config',
                    'properties': ['currentType'],
                    'filters': []
                }, {
                    'child':
                    'capture',
                    'properties': ['hardwareEnabled', 'softwareEnabled'],
                    'filters': []
                }, {
                    'child': '^(eth.*|novus.*|uhd.*|atlas.*|ares.*|star.*)$',
                    'properties': ['*'],
                    'filters': []
                }],
                'inlines': []
            }]
        }
        url = '%s/operations/select?xpath=true' % self._ixnetwork.href
        results = self._ixnetwork._connection._execute(url, payload)
        vports = {}
        if 'vport' in results[0]:
            for vport in results[0]['vport']:
                vports[vport['name']] = vport
        return vports

    def select_traffic_items(self, traffic_item_filters=[]):
        """Select all traffic items.
        Return them in a dict keyed by traffic item name.

        Args
        ----
        - filters (list(dict(property:'', 'regex':''))): A list of filters for the select.
            A filter is a dict with a property name and a regex match
        """
        payload = {
            'selects': [{
                'from':
                '/traffic',
                'properties': [],
                'children': [{
                    'child': 'trafficItem',
                    'properties': ['name', 'state', 'enabled'],
                    'filters': traffic_item_filters
                }, {
                    'child':
                    'highLevelStream',
                    'properties': ['txPortName', 'rxPortNames', 'state'],
                    'filters': []
                }],
                'inlines': []
            }]
        }
        url = '%s/operations/select?xpath=true' % self._ixnetwork.href
        results = self._ixnetwork._connection._execute(url, payload)
        traffic_items = {}
        try:
            for traffic_item in results[0]['trafficItem']:
                traffic_items[traffic_item['name']] = traffic_item
        except Exception:
            pass
        return traffic_items

    def select_chassis_card_port(self, location):
        """Select all availalehardware.
        Return them in a dict keyed by vport name.
        """
        (hostname, cardid, portid) = location.split(';')
        payload = {
            'selects': [{
                'from':
                '/availableHardware',
                'properties': [],
                'children': [{
                    'child':
                    'chassis',
                    'properties': [],
                    'filters': [{
                        'property': 'hostname',
                        'regex': '^%s$' % hostname
                    }]
                }, {
                    'child':
                    'card',
                    'properties': [],
                    'filters': [{
                        'property': 'cardId',
                        'regex': '^%s$' % abs(int(cardid))
                    }]
                }, {
                    'child':
                    'port',
                    'properties': [],
                    'filters': [{
                        'property': 'portId',
                        'regex': '^%s$' % abs(int(portid))
                    }]
                }],
                'inlines': []
            }]
        }
        url = '%s/operations/select?xpath=true' % self._ixnetwork.href
        results = self._ixnetwork._connection._execute(url, payload)
        return results[0]['chassis'][0]['card'][0]['port'][0]['xpath']

    def clear_ownership(self, available_hardware_hrefs, location_hrefs):
        """"""

    def get_config(self):
        return self._config

    def check_protocol_statistics(self):
        """"""

    def info(self, message):
        self._ixnetwork.info('[ixn-otg] %s' % message)

    def warning(self, message):
        self._ixnetwork.warn('[ixn-otg] %s' % message)
