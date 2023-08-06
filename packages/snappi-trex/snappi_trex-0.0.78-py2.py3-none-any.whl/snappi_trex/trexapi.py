import json
import snappi
from trex.stl.api import *
from snappi_trex.validation import Validation
from snappi_trex.setconfig import SetConfig


class Api(snappi.Api):
    """T-Rex implementation of the abstract-open-traffic-generator package

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
        self._c = STLClient()
        self._portIndices = {}
        

    # try to disconnect when object is deleted
    def __del__(self):
        try:
            self._c.disconnect()
        except STLError as e:
            print(e)


    # Maps port names used in Snappi to port index for T-Rex
    def _loadPorts(self):
        if 'ports' in self._cfg:
            i = 0
            for p in self._cfg['ports']:
                self._portIndices[p['name']] = i
                i += 1


    def set_config(self, config):
        """Set or update the configuration
        """
        self._cfg = json.loads(config.serialize())
        self._loadPorts()

        try:
            # connect to server
            self._c.connect()

            # prepare our ports
            self._c.reset(ports = list(self._portIndices.values()))

            # for each Snappi flow, construct the equivalent T-Rex stream
            for f in self._cfg["flows"]:
                
                # Configure variable manager commands
                vmCmds = []

                # Configure flow rate
                pps, bps, percent = SetConfig.set_rate(rate=f['rate'])

                # Configure duration and initialize the transmit mode using rate and duration info
                mode = SetConfig.set_duration(duration=f['duration'], pps=pps, bps=bps, percent=percent)

                # Parse config all packet headers. Creates a Scapy packet with provided packet headers
                headerCmds, pkt_headers, layers = SetConfig.set_packet_headers(f['packet'])
                vmCmds += headerCmds
                
                #Constructs the packet base using all headers
                pkt_base = None
                for header in pkt_headers:
                    pkt_base = header if pkt_base is None else pkt_base/header

                # Configure packet size: increment, random, or fixed
                sizeCmds, pad = SetConfig.set_packet_size(
                    fSize=f['size'], pkt_base=pkt_base, layers=layers
                )
                vmCmds += sizeCmds
                
                # TODO: Now fix the checksum of modified packets
                
                # Construct the packet with given Flow Variables
                vm = STLScVmRaw(vmCmds)
                pkt = STLPktBuilder(pkt = pkt_base/pad, vm = vm)

                # Create the stream with given config
                s1 = STLStream(packet = pkt,
                            mode = mode)

                # Add the stream to the client
                self._c.add_streams([s1], ports=[self._portIndices[f['tx_rx']['port']['tx_name']]])

        # Disconnect on error
        except STLError as e:
            self._c.disconnect()
            print(e)

        return {'warnings': []}


    def set_transmit_state(self, payload):
        """Set the transmit state of flows
        """
        try:
            # Clear stats
            self._c.clear_stats()

            # Start streams on all ports
            self._c.start(ports = list(self._portIndices.values()))

            # Wait until traffic stops
            self._c.wait_on_traffic(ports = list(self._portIndices.values()))

        except STLError as e:
            print(e)
        

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


    def get_config(self):
        return self._config

