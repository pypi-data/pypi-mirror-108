from __future__ import print_function

from .GlueSessionsConstants import *
from IPython.core.magic import Magics, cell_magic, line_magic, magics_class

@magics_class
class KernelMagics(Magics):

    def __init__(self, shell, data, kernel):
        super(KernelMagics, self).__init__(shell)
        self.data = data
        self.kernel = kernel

    @line_magic('iam_role')
    def set_iam_role(self, glue_role_arn):
        self._validate_magic()
        print(f'Current glue_role_arn is {self.kernel.get_glue_role_arn()}')
        self.kernel.set_glue_role_arn(glue_role_arn)
        print(f'IAM role has been set to {glue_role_arn}. Trying to re-authenticate.')
        new_client = self.kernel.authenticate(glue_role_arn=glue_role_arn, profile=self.kernel.get_profile())
        self.kernel.glue_client = new_client
        self.kernel.create_session()

    @line_magic('new_session')
    def new_session(self, line=None):
        self.kernel.delete_session()
        print(f'Creating new session.')
        new_client = self.kernel.authenticate(glue_role_arn=self.kernel.get_glue_role_arn(), profile=self.kernel.get_profile())
        self.kernel.glue_client = new_client
        self.kernel.create_session()

    @line_magic('profile')
    def set_profile(self, profile):
        self._validate_magic()
        print(f'Previous profile: {self.kernel.get_profile()}')
        print(f'Setting new profile to: {profile}')
        self.kernel.set_profile(profile)

    @line_magic('status')
    def get_status(self, line=None):
        status = self.kernel.get_current_session_status()
        duration = self.kernel.get_current_session_duration_in_seconds()
        role = self.kernel.get_current_session_role()
        print(f'Status: {status}')
        print(f'Duration: {duration} seconds')
        print(f'Role: {role}')

    @line_magic('list_sessions')
    def list_sessions(self, line=None):
        ids = self.kernel.get_sessions().get('Ids')
        print(f'There are currently {len(ids)} active sessions:')
        for id in ids:
            print(id)

    @line_magic('terminate_session')
    def terminate_session(self, line=None):
        self.kernel.delete_session()
        print(f'Terminated session.')

    @line_magic('session_id')
    def get_session_id(self, line=None):
        print(f'Current Session ID: {self.kernel.get_session_id()}')

    @line_magic('enable_glue_datacatalog')
    def set_enable_glue_datacatalog(self, line=None):
        self._validate_magic()
        print("Enabling Glue DataCatalog")
        self.kernel.set_enable_glue_datacatalog()

    @line_magic('extra_py_files')
    def set_extra_py_files(self, line=None):
        self._validate_magic()
        print("Adding the following:")
        for s3_path in line.split(','):
            print(s3_path)
        self.kernel.set_extra_py_files(line)

    @line_magic('additional_python_modules')
    def set_additional_python_modules(self, line=None):
        self._validate_magic()
        print("Adding the following:")
        for s3_path in line.split(','):
            print(s3_path)
        self.kernel.set_additional_python_modules(line)

    @line_magic('extra_jars')
    def set_extra_jars(self, line=None):
        self._validate_magic()
        print("Adding the following:")
        for s3_path in line.split(','):
            print(s3_path)
        self.kernel.set_extra_jars(line)

    @line_magic('temp_dir')
    def set_temp_dir(self, line=None):
        self._validate_magic()
        print(f"Setting temporary directory to: {line}")
        self.kernel.set_temp_dir(line)

    @line_magic('connections')
    def set_connections(self, line=None):
        self._validate_magic()
        print("Adding the following:")
        for connection in line.split(','):
            print(connection)
        self.kernel.set_connections(line)

    @line_magic('endpoint')
    def set_endpoint(self, line=None):
        print(f'Previous endpoint: {self.kernel.get_endpoint_url()}')
        print(f'Setting new endpoint to: {line}')
        self.kernel.set_endpoint_url(line)

    @line_magic('region')
    def set_region(self, line=None):
        self._validate_magic()
        print(f'Previous region: {self.kernel.get_region()}')
        print(f'Setting new region to: {line}')
        self.kernel.set_region(line)

    @line_magic('max_capacity')
    def set_max_capacity(self, line=None):
        self._validate_magic()
        print(f'Previous max capacity: {self.kernel.get_max_capacity()}')
        print(f'Setting new max capacity to: {float(line)}')
        self.kernel.set_max_capacity(line)

    @line_magic('number_of_workers')
    def set_number_of_workers(self, line=None):
        self._validate_magic()
        print(f'Previous number of workers: {self.kernel.get_number_of_workers()}')
        print(f'Setting new number of workers to: {int(line)}')
        self.kernel.set_number_of_workers(line)

    @line_magic('worker_type')
    def set_worker_type(self, line=None):
        self._validate_magic()
        print(f'Previous worker type: {self.kernel.get_worker_type()}')
        print(f'Setting new worker type to: {line}')
        self.kernel.set_worker_type(line)

    @line_magic('security_config')
    def set_security_config(self, line=None):
        self._validate_magic()
        print(f'Previous security_config: {self.kernel.get_security_config()}')
        print(f'Setting new security_config to: {line}')
        self.kernel.set_security_config(line)

    @line_magic('disconnect')
    def disconnect(self, line=None):
        self.kernel.disconnect()

    @line_magic('reconnect')
    def reconnect(self, line=None):
        self.kernel.reconnect(line)

    @cell_magic('sql')
    def run_sql(self, line=None, cell=None):
        if line == 'show':
            code = f'spark.sql(\'{cell.rstrip()}\').show()'
            self.kernel.do_execute(code, False, True, None, False)
        else:
            code = f'spark.sql(\'{cell.rstrip()}\')'
            self.kernel.do_execute(code, False, True, None, False)

    @cell_magic('configure')
    def configure(self, line=None, cell=None):
        self._validate_magic()
        self.kernel.configure(cell)

    @line_magic('help')
    def help(self, line=None):
        print(HELP_TEXT)

    def _validate_magic(self):
        session_id = self.kernel.get_session_id()
        if session_id:
            print(f"You are already connected to session {session_id}. Your change will not reflect in the current session, but it will affect future new sessions. \n")
