import os
import csv
from dataclasses import asdict
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from flask import Flask, jsonify, abort

# Import the model - support running as package or as a script
try:
    from .Models.customer_record import CustomerRecord
except Exception:
    from Models.customer_record import CustomerRecord


def resolve_csv_path() -> str:
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.normpath(os.path.join(base_dir, '..', '..', 'Data', 'WA_Fn-UseC_-Telco-Customer-Churn.csv'))
    return csv_path


def record_to_serializable(rec: CustomerRecord) -> dict:
    d = asdict(rec)
    for k, v in list(d.items()):
        # convert Enum members to their value
        if isinstance(v, Enum):
            d[k] = v.value
        # convert Decimal to float
        elif isinstance(v, Decimal):
            d[k] = float(v)
        # leave None as-is
    return d


def load_records() -> List[CustomerRecord]:
    path = resolve_csv_path()
    records: List[CustomerRecord] = []
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found at: {path}")

    with open(path, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rec = CustomerRecord.from_csv_row(row)
            except Exception:
                # if parsing fails for a row, skip it
                continue
            records.append(rec)

    return records


def create_app(test_config: Optional[dict] = None) -> Flask:
    app = Flask(__name__)

    # load data once at startup
    try:
        records = load_records()
    except Exception as e:
        # put empty list on failure but keep app running
        records = []

    app.config['RECORDS'] = records

    # register routes from Routes/records_routes.py
    from .Routes.records_routes import records_bp
    app.register_blueprint(records_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
