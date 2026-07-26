
import zcatalyst_sdk


def list_tables():
    try:
        # Initialize the app locally; it expects .catalystrc and valid CLI login
        app = zcatalyst_sdk.initialize()
        datastore = app.datastore()

        # We need to get all tables. The SDK might not have a direct list_tables method?
        # Wait, Python SDK might not have an easy way. Let's try getting one table.
        try:
            state_table = datastore.table_meta("State")
            print("State table exists:", state_table)
        except Exception as e:
            print("State table not found:", str(e))

    except Exception as e:
        print("Initialization error:", str(e))

if __name__ == "__main__":
    list_tables()
