# controllers/etl_controller.py
from models.extract import extract
from models.load import load
from models.transform import transform
from views.report import report

def run_etl():
    # Extract
    data = extract()
    data.extract_data()

    # Transform
    transformed_data = transform(data.get_data())

    # Load
    load(transformed_data)

    # Display
    view = report()
    view.display_report()