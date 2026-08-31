from flask import Blueprint, jsonify, abort, current_app, request
from ..Services.outreach_service import UpdateOutreachStatus
from ..Services.risk_score_service import GetAllRiskInformation

try:
    # relative import when running as package
    from ..main import record_to_serializable
except Exception:
    # fallback when running as script
    from main import record_to_serializable

records_bp = Blueprint('records', __name__)

def _apply_filters(records, filters):
    """Apply dynamic filters to records based on query parameters.

    Supported filter operators:
    - field=value (equality)
    - field__gt=value (greater than)
    - field__gte=value (greater than or equal)
    - field__lt=value (less than)
    - field__lte=value (less than or equal)
    - field__contains=value (contains substring)
    - field__startswith=value (starts with)
    - field__endswith=value (ends with)
    """
    if not filters:
        return records

    filtered_records = []

    for record in records:
        serialized = record_to_serializable(record)
        matches = True

        for filter_key, filter_value in filters.items():
            # Parse the filter key to extract field name and operator
            if '__' in filter_key:
                field_name, operator = filter_key.rsplit('__', 1)
            else:
                field_name = filter_key
                operator = 'eq'

            # Skip if field doesn't exist in record
            if field_name not in serialized:
                matches = False
                break

            record_value = serialized[field_name]

            try:
                # Apply the appropriate operator
                if operator == 'eq':  # Equality
                    if str(record_value).lower() != str(filter_value).lower():
                        matches = False
                        break

                elif operator == 'gt':  # Greater than
                    if float(record_value) <= float(filter_value):
                        matches = False
                        break

                elif operator == 'gte':  # Greater than or equal
                    if float(record_value) < float(filter_value):
                        matches = False
                        break

                elif operator == 'lt':  # Less than
                    if float(record_value) >= float(filter_value):
                        matches = False
                        break

                elif operator == 'lte':  # Less than or equal
                    if float(record_value) > float(filter_value):
                        matches = False
                        break

                elif operator == 'contains':  # Contains substring
                    if str(filter_value).lower() not in str(record_value).lower():
                        matches = False
                        break

                elif operator == 'startswith':  # Starts with
                    if not str(record_value).lower().startswith(str(filter_value).lower()):
                        matches = False
                        break

                elif operator == 'endswith':  # Ends with
                    if not str(record_value).lower().endswith(str(filter_value).lower()):
                        matches = False
                        break

            except (ValueError, AttributeError):
                # If conversion fails, treat as string comparison
                if str(record_value).lower() != str(filter_value).lower():
                    matches = False
                    break

        if matches:
            filtered_records.append(record)

    return filtered_records

@records_bp.route('/customers', methods=['GET'])
def get_records():
    allowed_fields = {'customer_id', 'outreach', 'tenure','contract' ,'monthly_charges', 'churn', 'risk_score'}

    # Extract filters from query parameters
    filters = {}
    for key, value in request.args.items():
        filters[key] = value

    # Apply filters to records
    filtered_records = _apply_filters(current_app.config['RECORDS'], filters)
    serialized = []
    for r in filtered_records:
        filtered = {k: v for k, v in record_to_serializable(r).items() if k in allowed_fields}
        # Convert boolean values to Yes/No
        for k, v in filtered.items():
            if isinstance(v, bool):
                filtered[k] = "Yes" if v else "No"
        serialized.append(filtered)
    return jsonify(serialized)

def _convert_record_values(record_dict):
    """Convert boolean and list values in a record dictionary."""
    for k, v in record_dict.items():
        if isinstance(v, bool):
            record_dict[k] = "Yes" if v else "No"
        elif isinstance(v, list):
            # Convert list items to strings and join them
            record_dict[k] = "; ".join(str(item) for item in v)
    return record_dict

@records_bp.route('/customers/<customer_id>', methods=['GET'])
def get_record(customer_id: str):
    for r in current_app.config['RECORDS']:
        if getattr(r, 'customer_id', None) == customer_id:
            customer_record = record_to_serializable(r)
            customer_record = _convert_record_values(customer_record)
            return jsonify(customer_record)
    abort(404)

@records_bp.route('/customers/<customer_id>/outreach', methods=['PATCH'])
def update_outreach_status(customer_id: str):
    for i, r in enumerate(current_app.config['RECORDS']):
        if getattr(r, 'customer_id', None) == customer_id:
            updated_record = UpdateOutreachStatus(r)
            # Update the record in memory
            current_app.config['RECORDS'][i] = updated_record

            customer_record = record_to_serializable(updated_record)
            customer_record = _convert_record_values(customer_record)
            return jsonify(customer_record)
    abort(404)

@records_bp.route('/model/info', methods=['GET'])
def get_model_info():
    """Return all risk information as a JSON-serializable list.

    GetAllRiskInformation may return objects, dicts, or other types. Normalize
    the output to a list of plain dicts/primitives so Flask's jsonify can
    serialize it reliably for the frontend.
    """
    risk_informations = GetAllRiskInformation()

    if not risk_informations:
        return jsonify([])

    normalized = []

    # If service returned a single dict-like mapping containing an items list,
    # prefer that list.
    if isinstance(risk_informations, dict):
        if isinstance(risk_informations.get('items'), (list, tuple)):
            iterable = risk_informations['items']
        else:
            # Fall back to the dict's values
            iterable = list(risk_informations.values())
    else:
        iterable = risk_informations

    # Ensure we have a sequence to iterate over
    if not isinstance(iterable, (list, tuple)):
        iterable = [iterable]

    for item in iterable:
        if item is None:
            continue
        if isinstance(item, dict):
            normalized.append(item)
            continue

        # Try to convert domain objects to serializable dicts using
        # record_to_serializable (imported above). If that fails, fall back to
        # converting the object to a string value.
        try:
            obj = record_to_serializable(item)
            normalized.append(obj)
        except Exception:
            try:
                # Some objects may implement __dict__ or dataclass-like mapping
                if hasattr(item, '__dict__'):
                    normalized.append({k: v for k, v in vars(item).items()})
                else:
                    normalized.append({'value': str(item)})
            except Exception:
                normalized.append({'value': str(item)})

    return jsonify(normalized)
