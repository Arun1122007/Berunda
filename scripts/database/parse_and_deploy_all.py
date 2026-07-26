
def parse_markdown_schema():
    with open('docs/database/CATALYST_DATASTORE_SCHEMA_MAPPING.md') as f:
        lines = f.readlines()

    tables = []
    current_table = None

    for line in lines:
        if line.strip().startswith('|') and 'Catalyst Table' not in line and '---' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 8:
                continue

            er_table = parts[1]
            cat_table = parts[2]
            er_field = parts[3]
            cat_field = parts[4]
            col_type = parts[5].lower()
            parent_table = parts[6]
            constraints = parts[7].lower()
            on_delete = parts[8].lower()

            if cat_table:
                current_table = {'tableName': cat_table, 'columns': []}
                tables.append(current_table)

            if not cat_field:
                continue

            col = {
                'columnName': cat_field,
                'dataType': 'varchar'
            }

            if 'int' in col_type and 'bigint' not in col_type:
                col['dataType'] = 'int'
            elif 'bigint' in col_type:
                col['dataType'] = 'bigint'
            elif 'date' in col_type and 'datetime' not in col_type:
                col['dataType'] = 'date'
            elif 'datetime' in col_type:
                col['dataType'] = 'datetime'
            elif 'double' in col_type:
                col['dataType'] = 'double'
            elif 'boolean' in col_type:
                col['dataType'] = 'boolean'
            elif 'encrypted text' in col_type:
                col['dataType'] = 'encrypted text'
            elif 'foreign key' in col_type:
                col['dataType'] = 'foreign key'
                col['parentTable'] = parent_table
                col['onDelete'] = 'cascade' if 'cascade' in on_delete else 'restrict'

            if 'mandatory' in constraints:
                col['isMandatory'] = True
            if 'unique' in constraints:
                col['isUnique'] = True

            current_table['columns'].append(col)

    return tables

def deploy_schema():
    schema = parse_markdown_schema()

    headers = {
        "accept": "application/vnd.catalyst.v2+json",
        "catalyst-org": "60079736152",
        "cookie": "__Secure-iamsdt=0.CAESdBIwzmTMrwuP8uj3WTkU4gtsgODsao7JXPskpYvvxIbiFyAbOdG623V4W3N_2sMGz5cNGkACOFEaCIrh_VrH2uMyorQIDeke5zp5ggt6bCHZCqqULpTy8NoJO-VNuEP6nMAlHRMzt05tfpebdwaig3VcH5sBIJ_jrqqW0NbpRw; _iamadt=ce64ccaf0b8ff2e8f7593914e20b6c80e0ec6a8ec95cfb24a58befc486e217201b39d1badb75785b737fdac306cf970d; _iambdt=0238511a088ae1fd5ac7dae332a2b4080de91ee73a79820b7a6c21d90aaa942e94f2f0da093be54db843fa9cc0251d1333b74e6d7e979b7706a283755c1f9b01; wms-tkp-token=60078390577-04f46b28-9bf597d960729ef374d9f5e933fc8b3f; zalb_3a750b85f1=ed010f63633be60a322039283f31a645; ZD_CSRF_TOKEN=1fd540491953de3a080808f846ae5a1c75caae7a5bdff13bd83286485f512c53020070a9fd7ac53c98505b7bc5df531f2a429b0f88269cfc3a2d532e781e4640; JSESSIONID=8E06C205DBE4F987A7CB6DA15E725D58; zalb_bc5826c95a=e7d38d023778301e53393866fb229e58; CT_CSRF_TOKEN=1fd540491953de3a080808f846ae5a1c75caae7a5bdff13bd83286485f512c53020070a9fd7ac53c98505b7bc5df531f2a429b0f88269cfc3a2d532e781e4640; zalb_zid=60079736152",
        "x-zcsrf-token": "zd_csrparam=1fd540491953de3a080808f846ae5a1c75caae7a5bdff13bd83286485f512c53020070a9fd7ac53c98505b7bc5df531f2a429b0f88269cfc3a2d532e781e4640",
    }

    print(f"Parsed {len(schema)} tables from Markdown.")

if __name__ == '__main__':
    deploy_schema()
