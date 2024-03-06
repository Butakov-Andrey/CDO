import csv


def create_csv(model_objects, model):
    csv_file_path = f"/{model.__tablename__}.csv"
    field_names = list(model.__table__.columns.keys())
    with open(csv_file_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(field_names)
        [
            csv_writer.writerow(
                [
                    getattr(model_object, column.name)
                    for column in model.__mapper__.columns
                ]
            )
            for model_object in model_objects
        ]
    return csv_file_path
