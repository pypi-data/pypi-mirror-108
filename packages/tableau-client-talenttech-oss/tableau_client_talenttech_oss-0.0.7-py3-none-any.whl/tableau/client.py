import logging
import tableauserverclient as TSC
import sys


class Client:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
    logging.captureWarnings(True)

    def __init__(
            self,
            url_server_tableau,
            user_name_tableau,
            password_tableau,
            url_site

    ):
        self.url_server_tableau = url_server_tableau
        self.password_tableau = password_tableau
        self.user_name_tableau = user_name_tableau
        self.url_site = url_site
        self.connect_to_server()

    def connect_to_server(
            self
    ):
        """
        init server tableau connection
        :return: server tableau connection
        """
        self.status_connection = False
        logging.info('try connect to server')
        try:
            tableau_auth = TSC.TableauAuth(self.user_name_tableau, self.password_tableau, self.url_site)
            self.server = TSC.Server(self.url_server_tableau, use_server_version=True)
            self.server_auth = self.server.auth.sign_in(tableau_auth)
            self.status_connection = True
        except:
            logging.info('error connecting to server')

    def get_dashboard_id(
            self,
            workbook_id
    ):
        try:
            if self.url_site == '':
                number_id = 5
            else:
                number_id = 7
            workbook_id = int(workbook_id)

            if self.status_connection:
                with self.server_auth:
                    self.workbook_id = 0
                    self.workbook_name = ''
                    all_datasource, all_pagination = self.server.workbooks.get()
                    for workbooks in all_datasource:
                        if int(workbooks.webpage_url.split('/')[number_id]) == workbook_id:
                            self.workbook_id =workbooks.id
                            self.workbook_name =workbooks.name
                if self.workbook_id == 0:
                    logging.info('Dashboard id ' + str(workbook_id) + ' not found on server')
        except:
            self.workbook_id =0
            logging.info('Workbook id must be numeric')

    def dashboard_refresh(
            self,
            workbook_id
    ):
        """
        start jobs extract refresh for dashboard
        """
        if self.status_connection:
            self.get_dashboard_id(workbook_id)
            self.connect_to_server()

            if self.workbook_id != 0:
                with self.server_auth:
                    try:
                        result = self.server.workbooks.refresh(self.workbook_id)
                        logging.info('Dashboard start updating on '+str(result.created_at))
                    except:
                        logging.info('Dashboard '+self.workbook_name +' extract refresh is already starting')

    def view_to_csv(
            self,
            workbook_name,
            sheet_name,
            csv_path,
    ):
        """
        export view to csv file
        """
        self.get_dashboard_id(workbook_name)
        self.connect_to_server()
        is_found = False
        if self.workbook_id > 0:
            with self.server_auth:
                try:
                    workbook = self.server.workbooks.get_by_id(self.workbook_id)
                    for view in workbook.views:
                        if view.name == sheet_name:
                            self.server.views.populate_csv(view)
                            with open(csv_path, 'wb') as f:
                                f.write(b''.join(view.csv))
                                logging.info('View ' + sheet_name + ' export to csv')
                                is_found = True
                    if is_found == False:
                        logging.info('View ' + sheet_name +' not found in workbook '+workbook_name)
                except:
                    logging.info('Error!')