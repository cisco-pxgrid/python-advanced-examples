import argparse
import ssl


class CreateAccountConfig:
    def __init__(self):
        self.__ssl_context = None
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-a', '--hostname', required=True,
            help='ISE PAN host name')
        parser.add_argument(
            '--username', required=True,
            help='ISE username')
        parser.add_argument(
            '--password', required=True,
            help='ISE password')
        parser.add_argument(
            '--nodename', required=True,
            help='Client node name to create and approve')
        parser.add_argument(
            '--description', type=str,
            default='pxGrid Client',
            help='Optional description for the pxGrid client/node')

        g = parser.add_mutually_exclusive_group()
        g.add_argument(
            '-s', '--servercert',
            help='Server certificates pem filename')
        g.add_argument(
            '--insecure', action='store_true',
            help='Allow insecure server connections when using SSL')

        parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='Verbose output')
        self.config = parser.parse_args()

    @property
    def hostname(self):
        return self.config.hostname

    @property
    def username(self):
        return self.config.username

    @property
    def password(self):
        return self.config.password

    @property
    def nodename(self):
        return self.config.nodename

    @property
    def description(self):
        return self.config.description

    @property
    def servercert(self):
        return self.config.servercert

    @property
    def insecure(self):
        return self.config.insecure

    @property
    def verbose(self):
        return self.config.verbose

    @property
    def ssl_context(self):
        if self.__ssl_context == None:
            self.__ssl_context = ssl.create_default_context()
            if self.config.servercert:
                self.__ssl_context.load_verify_locations(cafile=self.config.servercert)
            elif self.config.insecure:
                self.__ssl_context.check_hostname = False
                self.__ssl_context.verify_mode = ssl.CERT_NONE
        return self.__ssl_context
