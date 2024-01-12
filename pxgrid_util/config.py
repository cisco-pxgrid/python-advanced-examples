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

def ensure_parsed(func):
    def wrapper(instance):
        instance.parse_args()
        return func(instance)
    return wrapper


class Config:
    args_parsed = False

    def __init__(self):
        self.__ssl_context = None

        #
        # Options that apply to all clients. `parser` is now member variable
        # so that users can extend the parser in their own scripts with their
        # own options and explicitly invoke `parse`
        #
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-a', '--hostname',
            help='pxGrid controller host name (multiple ok)',
            action='append')
        self.parser.add_argument(
            '--port',
            help='pxGrid port (default 8910)',
            default=8910)
        self.parser.add_argument(
            '-n', '--nodename',
            help='Client node name')
        self.parser.add_argument(
            '-w', '--password',
            help='Password (optional)')
        self.parser.add_argument(
            '-d', '--description',
            help='Description (optional)')
        self.parser.add_argument(
            '-c', '--clientcert',
            help='Client certificate chain pem filename (optional)')
        self.parser.add_argument(
            '-k', '--clientkey',
            help='Client key filename (optional)')
        self.parser.add_argument(
            '-p', '--clientkeypassword',
            help='Client key password (optional)')
        self.parser.add_argument(
            '-s', '--servercert',
            help='Server certificates pem filename')
        self.parser.add_argument(
            '--insecure', action='store_true',
            help='Allow insecure server connections when using SSL')
        self.parser.add_argument(
            '--discovery-override', type=str,
            help='Override pxGrid service discovery (for test environments without proper DNS)')
        self.parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='Verbose output')

        #
        # Options that apply to `px-subscribe` only
        #
        self.parser.add_argument(
            '--ws-ping-interval', type=float,
            default=20.0,
            help='WebSocket ping interval in seconds (float)')
        self.parser.add_argument(
            '--service', type=str,
            help='Service name')
        self.parser.add_argument(
            '--topic', type=str,
            help='Topic to subscribe to')
        self.parser.add_argument(
            '--subscribe', action='store_true',
            help='set up a subscription')
        self.parser.add_argument(
            '--subscribe-all', action='store_true',
            help='subscribe to ALL nodes discovered')

        # optionally select a subscriber that is not the default one
        g = self.parser.add_mutually_exclusive_group()
        g.add_argument(
            '--connect-only', action='store_true',
            help='connect to pxGrid brokers only, no subscription')
        g.add_argument(
            '--session-dedup', action='store_true',
            help='run the sessionTopic de-duplicating subscriber')

        self.parser.add_argument(
            '--services', action='store_true',
            help='List out supported services')
        self.parser.add_argument(
            '--service-details', type=str,
            help='List out details of a specific service')

        #
        # Options that apply to populating session directory queries
        #
        self.parser.add_argument(
            '--ip', type=str,
            help='Optional IP address for queries')
        self.parser.add_argument(
            '--start-timestamp', type=str,
            help='Optional startTimestamp for queries')

        #
        # Options for getting, applying and clearing ANC policies via
        # `anc-policy`
        #
        g = self.parser.add_mutually_exclusive_group()
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
            '--apply-anc-policy-by-mac-bulk', type=str,
            help='Bulk-apply named ANC policy by endpoint MAC addresses in flat file')
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
        self.parser.add_argument(
            '--anc-policy', type=str,
            help='Optional ANC policy name')
        self.parser.add_argument(
            '--anc-mac-address', type=str,
            help='Optional MAC address for ANC policies')
        self.parser.add_argument(
            '--anc-ip-address', type=str,
            help='Optional IP address for ANC policies')
        self.parser.add_argument(
            '--anc-nas-ip-address', type=str,
            help='Optional NAS IP address for ANC policies')
        self.parser.add_argument(
            '--anc-policy-action', type=AncPolicyType,
            choices=list(AncPolicyType))

        # publishing parameters
        self.parser.add_argument(
            '--publish-delay', type=float, default=1.0,
            help='delay between custom event publishes')
        self.parser.add_argument(
            '--reregister-delay', type=float, default=1.0,
            help='delay between custom service reregistrations')

    def parse_args(self):
        '''
        Call this function after you have 
        '''
        if not self.args_parsed:
            self.config = self.parser.parse_args()
            self.args_parsed = True

    @property
    @ensure_parsed
    def subscribe(self):
        return self.config.subscribe

    @property
    @ensure_parsed
    def subscribe_all(self):
        return self.config.subscribe_all

    @property
    @ensure_parsed
    def connect_only(self):
        return self.config.connect_only

    @property
    @ensure_parsed
    def session_dedup(self):
        return self.config.session_dedup

    @property
    @ensure_parsed
    def ws_ping_interval(self):
        return self.config.ws_ping_interval

    @property
    @ensure_parsed
    def services(self):
        return self.config.services

    @property
    @ensure_parsed
    def service_details(self):
        return self.config.service_details

    @property
    @ensure_parsed
    def verbose(self):
        return self.config.verbose

    @property
    @ensure_parsed
    def hostname(self):
        return self.config.hostname

    @property
    @ensure_parsed
    def port(self):
        return self.config.port

    @property
    @ensure_parsed
    def node_name(self):
        return self.config.nodename

    @property
    @ensure_parsed
    def password(self):
        if self.config.password is not None:
            return self.config.password
        else:
            return ''

    @property
    @ensure_parsed
    def discovery_override(self):
        return self.config.discovery_override

    @property
    @ensure_parsed
    def service(self):
        return self.config.service

    @property
    @ensure_parsed
    def topic(self):
        return self.config.topic

    @property
    @ensure_parsed
    def ip(self):
        return self.config.ip

    @property
    @ensure_parsed
    def start_timestamp(self):
        return self.config.start_timestamp

    @property
    @ensure_parsed
    def get_anc_endpoints(self):
        return self.config.get_anc_endpoints
        
    @property
    @ensure_parsed
    def get_anc_policy_by_mac(self):
        return self.config.get_anc_policy_by_mac
        
    @property
    @ensure_parsed
    def get_anc_policies(self):
        return self.config.get_anc_policies
        
    @property
    @ensure_parsed
    def apply_anc_policy(self):
        return self.config.apply_anc_policy
        
    @property 
    @ensure_parsed
    def apply_anc_policy_by_mac(self):
        return self.config.apply_anc_policy_by_mac
        
    @property 
    @ensure_parsed
    def apply_anc_policy_by_mac_bulk(self):
        return self.config.apply_anc_policy_by_mac_bulk
        
    @property
    @ensure_parsed
    def apply_anc_policy_by_ip(self):
        return self.config.apply_anc_policy_by_ip
        
    @property
    @ensure_parsed
    def clear_anc_policy_by_mac(self):
        return self.config.clear_anc_policy_by_mac
        
    @property
    @ensure_parsed
    def clear_anc_policy_by_ip(self):
        return self.config.clear_anc_policy_by_ip
        
    @property
    @ensure_parsed
    def create_anc_policy(self):
        return self.config.create_anc_policy
        
    @property
    @ensure_parsed
    def delete_anc_policy(self):
        return self.config.delete_anc_policy
        
    @property
    @ensure_parsed
    def anc_mac_address(self):
        return self.config.anc_mac_address

    @property
    @ensure_parsed
    def anc_policy(self):
        return self.config.anc_policy

    @property
    @ensure_parsed
    def anc_ip_address(self):
        return self.config.anc_ip_address

    @property
    @ensure_parsed
    def anc_nas_ip_address(self):
        return self.config.anc_nas_ip_address

    @property
    @ensure_parsed
    def anc_policy_action(self):
        return self.config.anc_policy_action

    @property
    @ensure_parsed
    def publish_delay(self):
        return self.config.publish_delay

    @property
    @ensure_parsed
    def reregister_delay(self):
        return self.config.reregister_delay

    @property
    @ensure_parsed
    def description(self):
        return self.config.description

    @property
    @ensure_parsed
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
