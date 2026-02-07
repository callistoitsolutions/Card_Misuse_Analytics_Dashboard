import yaml
from sqlalchemy import create_engine

def load_to_db(df, source_file):
    """
    Load a DataFrame into MySQL 'transactions_standard' table.
    Automatically adds 'source_file' column.
    """

    # Load config
    try:
        with open("config/db_config.yaml") as f:
            cfg = yaml.safe_load(f).get("mysql")
            if cfg is None:
                raise KeyError("The 'mysql' key is missing in db_config.yaml!")
    except FileNotFoundError:
        raise FileNotFoundError("❌ config/db_config.yaml not found!")
    except yaml.YAMLError as e:
        raise ValueError(f"❌ Error parsing YAML file: {e}")

    # Create SQLAlchemy engine
    engine = create_engine(
        f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}/{cfg['database']}"
    )

    # Add source file info
    df["source_file"] = source_file

    # Load into database
    try:
        df.to_sql(
            "transactions_standard",
            engine,
            if_exists="append",
            index=False
        )
        print(f"✅ Data loaded to database from file: {source_file}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load data into MySQL: {e}")
