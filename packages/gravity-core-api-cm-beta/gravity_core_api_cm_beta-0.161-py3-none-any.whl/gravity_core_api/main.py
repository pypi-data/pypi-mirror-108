""" Перспективный единый TCP API endpoint для Gravity core """
from witapi.main import WITServer
from gravity_core_api.wserver_update_commands.main import operate_update_record
from gravity_core_api.operate_user_commands.main import operate_user_command
from gravity_core_api import functions as general_functions
from gravity_core_api.general_methods import methods_dict
from traceback import format_exc


class GCSE(WITServer):
    """ Gravity Core Single Endpoint """

    def __init__(self, myip, myport, sqlshell, core, debug=False, without_auth=True, mark_disconnect=False, *args,
                 **kwargs):
        super().__init__(myip, myport, sqlshell=sqlshell, without_auth=without_auth, mark_disconnect=mark_disconnect,
                         debug=debug)
        self.core = core
        self.sqlshell = sqlshell
        self.core_support_methods = general_functions.extract_core_support_methods(core)

    def execute_command(self, comm, values, connection, *args, **kwargs):
        """ Выполнить метод, если он опеределен в methods_dict"""
        try:
            subcommand_operator = methods_dict[comm]['subcommand_operator']
            response = subcommand_operator(self.sqlshell, self.core_support_methods, comm, values)
        except IndexError:
            response = super().execute_command(comm, values, connection, *args, **kwargs)
        return response
