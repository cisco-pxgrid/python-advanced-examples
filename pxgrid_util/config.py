import argparse
import ssl
import enum


class AncPolicyType(enum.Enum):
    quarantine = 'QUARANTINE'
    shutdown = 'SHUT_DOWN'
    port_bounce = 'PORT_BOUNCE'
    reauthenticate = 'RE_AUTHENTICATE'

    def __str__(self):
        return self.value


class Config:
    def __init__(self):
        self.__ssl_context = None
        parser = argparse.ArgumentParser()

        #
        # Options that apply to all clients
        #
        parser.add_argument(
            '-a', '--hostname',
            help='pxGrid controller host name (multiple ok)',
            action='append')
        parser.add_argument(
            '--port',
            help='pxGrid port (default 8910)',
            default=8910)
        parser.add_argument(
            '-n', '--nodename',
            help='Client node name')
        parser.add_argument(
            '-w', '--password',
            help='Password (optional)')
        parser.add_argument(
            '-d', '--description',
            help='Description (optional)')
        parser.add_argument(
            '-c', '--clientcert',
            help='Client certificate chain pem filename (optional)')
        parser.add_argument(
            '-k', '--clientkey',
            help='Client key filename (optional)')
        parser.add_argument(
            '-p', '--clientkeypassword',
            help='Client key password (optional)')
        parser.add_argument(
            '-s', '--servercert',
            help='Server certificates pem filename')
        parser.add_argument(
            '--insecure', action='store_true',
            help='Allow insecure server connections when using SSL')
        parser.add_argument(
            '--discovery-override', type=str,
            help='Override pxGrid service discovery (for test environments without proper DNS)')
        parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='Verbose output')

        #
        # Options that apply to `px-subscribe` only
        #
        parser.add_argument(
            '--ws-ping-interval', type=float,
            default=20.0,
            help='WebSocket ping interval in seconds (float)')
        parser.add_argument(
            '--service', type=str,
            help='Service name')
        parser.add_argument(
            '--topic', type=str,
            help='Topic to subscribe to')
        parser.add_argument(
            '--subscribe', action='store_true',
            help='set up a subscription')
        parser.add_argument(
            '--subscribe-all', action='store_true',
            help='subscribe to ALL nodes discovered')

        # optionally select a subscriber that is not the default one
        g = parser.add_mutually_exclusive_group()
        g.add_argument(
            '--connect-only', action='store_true',
            help='connect to pxGrid brokers only, no subscription')
        g.add_argument(
            '--session-dedup', action='store_true',
            help='run the sessionTopic de-duplicating subscriber')

        parser.add_argument(
            '--services', action='store_true',
            help='List out supported services')
        parser.add_argument(
            '--service-details', type=str,
            help='List out details of a specific service')

        #
        # Options that apply to populating session directory queries
        #
        parser.add_argument(
            '--ip', type=str,
            help='Optional IP address for queries')
        parser.add_argument(
            '--start-timestamp', type=str,
            help='Optional startTimestamp for queries')

        #
        # Options that apply to `system-query-all` only
        #
        g = parser.add_mutually_exclusive_group()
        g.add_argument(
            '--get-system-health', action='store_true',
            help='Get all system health objects')
        g.add_argument(
            '--get-system-performance', action='store_true',
            help='Get all system performance objects')

        #
        # Options for getting, applying and clearing ANC policies via
        # `anc-policy`
        #
        g = parser.add_mutually_exclusive_group()
        g.add_argument(
            '--get-anc-endpoints', action='store_true',
            help='Get endpoints with ANC policies')
        g.add_argument(
            '--get-anc-policy-by-mac', action='store_true',
            help='Get endpoint\'s ANC policy by MAC address')
        g.add_argument(
            '--get-anc-policies', action='store_true',
            help='Get all ANC policies')
        g.add_argument(
            '--apply-anc-policy-by-mac', action='store_true',
            help='Apply named ANC policy by endpoint MAC address')
        g.add_argument(
            '--apply-anc-policy-by-ip', action='store_true',
            help='Apply named ANC policy by endpoint IP address')
        g.add_argument(
            '--apply-anc-policy', action='store_true',
            help='Apply named ANC policy by whatever parameters provided if there are enough')
        g.add_argument(
            '--clear-anc-policy-by-mac', action='store_true',
            help='Clear ANC policy by endpoint MAC address')
        g.add_argument(
            '--clear-anc-policy-by-ip', action='store_true',
            help='Clear ANC policy by endpoint IP address')
        g.add_argument(
            '--create-anc-policy', type=str,
            help='Create named ANC policy')
        g.add_argument(
            '--delete-anc-policy', type=str,
            help='Delete named ANC policy')

        # anc parameters
        parser.add_argument(
            '--anc-policy', type=str,
            help='Optional ANC policy name')
        parser.add_argument(
            '--anc-mac-address', type=str,
            help='Optional MAC address for ANC policies')
        parser.add_argument(
            '--anc-ip-address', type=str,
            help='Optional IP address for ANC policies')
        parser.add_argument(
            '--anc-nas-ip-address', type=str,
            help='Optional NAS IP address for ANC policies')
        parser.add_argument(
            '--anc-policy-action', type=AncPolicyType,
            choices=list(AncPolicyType))

        self.config = parser.parse_args()

    @property
    def subscribe(self):
        return self.config.subscribe

    @property
    def subscribe_all(self):
        return self.config.subscribe_all

    @property
    def connect_only(self):
        return self.config.connect_only

    @property
    def session_dedup(self):
        return self.config.session_dedup

    @property
    def ws_ping_interval(self):
        return self.config.ws_ping_interval

    @property
    def services(self):
        return self.config.services

    @property
    def service_details(self):
        return self.config.service_details

    @property
    def verbose(self):
        return self.config.verbose

    @property
    def hostname(self):
        return self.config.hostname

    @property
    def port(self):
        return self.config.port

    @property
    def node_name(self):
        return self.config.nodename

    @property
    def password(self):
        if self.config.password is not None:
            return self.config.password
        else:
            return ''

    @property
    def discovery_override(self):
        return self.config.discovery_override

    @property
    def service(self):
        return self.config.service

    @property
    def topic(self):
        return self.config.topic

    @property
    def ip(self):
        return self.config.ip

    @property
    def start_timestamp(self):
        return self.config.start_timestamp

    @property
    def get_system_health(self):
        return self.config.get_system_health
        
    @property
    def get_system_performance(self):
        return self.config.get_system_performance
        
    @property
    def get_anc_endpoints(self):
        return self.config.get_anc_endpoints
        
    @property
    def get_anc_policy_by_mac(self):
        return self.config.get_anc_policy_by_mac
        
    @property
    def get_anc_policies(self):
        return self.config.get_anc_policies
        
    @property
    def apply_anc_policy(self):
        return self.config.apply_anc_policy
        
    @property 
    def apply_anc_policy_by_mac(self):
        return self.config.apply_anc_policy_by_mac
        
    @property
    def apply_anc_policy_by_ip(self):
        return self.config.apply_anc_policy_by_ip
        
    @property
    def clear_anc_policy_by_mac(self):
        return self.config.clear_anc_policy_by_mac
        
    @property
    def clear_anc_policy_by_ip(self):
        return self.config.clear_anc_policy_by_ip
        
    @property
    def create_anc_policy(self):
        return self.config.create_anc_policy
        
    @property
    def delete_anc_policy(self):
        return self.config.delete_anc_policy
        
    @property
    def anc_mac_address(self):
        return self.config.anc_mac_address

    @property
    def anc_policy(self):
        return self.config.anc_policy

    @property
    def anc_ip_address(self):
        return self.config.anc_ip_address

    @property
    def anc_nas_ip_address(self):
        return self.config.anc_nas_ip_address

    @property
    def anc_policy_action(self):
        return self.config.anc_policy_action

    @property
    def description(self):
        return self.config.description

    @property
    def ssl_context(self):
        if self.__ssl_context == None:
            self.__ssl_context = ssl.create_default_context()
            if self.config.clientcert is not None:
                self.__ssl_context.load_cert_chain(
                    certfile=self.config.clientcert,
                    keyfile=self.config.clientkey,
                    password=self.config.clientkeypassword)
            if self.config.servercert:
                self.__ssl_context.load_verify_locations(cafile=self.config.servercert)
            elif self.config.insecure:
                self.__ssl_context.check_hostname = False
                self.__ssl_context.verify_mode = ssl.CERT_NONE
        return self.__ssl_context
