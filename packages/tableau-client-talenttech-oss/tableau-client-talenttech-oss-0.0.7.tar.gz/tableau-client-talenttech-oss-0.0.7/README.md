Tableau dashboard client


Install
```sh
pip tableau-client-talenttech-oss
```

```python
from tableau.client import Client

#initial connection to server tableau
tableau_client = Client(url_server_tableau='https://example.org/',
                        user_name_tableau='',
                        password_tableau='',
                        url_site=''
                        )

# update extract refresh for tableau workbook
# workbook_id - id published tableau workbook on server in url
tableau_client.dashboard_refresh(workbook_id =1)

# export sheet tableau workbook to csv file
# sheet_name - name worksheet in tableau workbook (workbook_name)
# csv_path - path with file name to save sheet_name to csv 
tableau_client.view_to_csv(workbook_name='',
                           sheet_name='',
                           csv_path='./view_data.csv'
                           )
```