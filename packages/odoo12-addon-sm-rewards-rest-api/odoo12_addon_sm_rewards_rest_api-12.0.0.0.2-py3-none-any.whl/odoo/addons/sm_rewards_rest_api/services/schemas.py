def boolean_validator(field, value, error):
  if value and value not in ["true", "false"]:
    error(field, "Must be a boolean value: true or false")

def date_validator(field, value, error):
  try:
    Date.from_string(value)
  except ValueError:
    return error(
        field, _("{} does not match format '%Y-%m-%d'".format(value))
    )

### CS REGISTRATION REQUEST SCHEMAS ###

S_SM_REWARD_GET = {"_id": {"type": "integer"}}

S_SM_REWARD_RETURN_GET = {
  "id": {"type": "integer", "required": True},
  "name": {"type": "string", "required": True},
  "reward_type": {"type": "string", "required": True}, # selection
  "promo_code": {"type": "string"},
  "related_analytic_account_id": {"type": "string"},
  "reward_date": {"type": "string", "regex": "\\d{4}-[01]\\d-[0-3]\\d"},
  "reward_addtime": {"type": "integer"},
  "reward_addmoney": {"type": "float"},
  "reward_info": {"type": "string"},
  "force_register_cs": {"type": "boolean"},
  "force_dedicated_ba": {"type": "boolean"},
  "coupon_group": {"type": "string"},
  "coupon_group_secondary": {"type": "string"},
  "tariff_name": {"type": "string"},
  "tariff_related_model": {"type": "string"},
  "tariff_type": {"type": "string"},
  "tariff_quantity": {"type": "string"},
  "maintenance_reservation_type": {"type": "string"}, # selection
  "maintenance_forgive_reservation": {"type": "boolean"},
  "maintenance_type": {"type": "string"}, # selection
  "maintenance_duration": {"type": "string"},
  "maintenance_observations": {"type": "string"},
  "maintenance_carconfig_index": {"type": "string"},
  "maintenance_carconfig_home": {"type": "string"},
  "maintenance_cs_person_index": {"type": "string"},
  "maintenance_reservation_start": {"type": "string"},
  "maintenance_car_plate": {"type": "string"},
  "maintenance_create_car_service": {"type": "boolean"},
  "maintenance_car_service_id": {"type": "string"},
  "maintenance_discount_reservation": {"type": "boolean"},
  "data_partner_creation_type": {"type": "string", "required": True}, # selection
  "data_partner_cs_user_type": {"type": "string"}, # selection
  "data_partner_firstname": {"type": "string"},
  "data_partner_lastname": {"type": "string"},
  "data_partner_vat": {"type": "string"},
  "data_partner_email": {"type": "string"},
  "data_partner_mobile": {"type": "string"},
  "data_partner_phone": {"type": "string"},
  "data_partner_gender": {"type": "string"}, # selection
  "data_partner_birthdate_date": {
    "type": "string", 
    "regex": "\\d{4}-[01]\\d-[0-3]\\d"
  },
  "data_partner_street": {"type": "string"},
  "data_partner_zip": {"type": "string"},
  "data_partner_state_id": {"type": "string"},
  "data_partner_city": {"type": "string"},
  "data_partner_iban": {"type": "string"},
  "data_partner_driving_license_expiration_date": {
    "type": "string",
    "regex": "\\d{4}-[01]\\d-[0-3]\\d"
    },
  "data_partner_image_dni": {"type": "string"},
  "data_partner_image_driving_license": {"type": "string"},
  "external_obj_id": {"type": "integer"},
  "external_promo_obj_id": {"type": "integer"},
  "state": {"type": "string"},
  "final_state": {"type": "string"}
}


S_SM_REWARD_CREATE = {
  "name": {"type": "string", "required": True},
  "reward_type": {"type": "string", "required": True}, # selection
  "promo_code": {"type": "string"},
  "related_analytic_account": {"type": "string"},
  "reward_date": {"type": "string", "regex": "\\d{4}-[01]\\d-[0-3]\\d"},
  "reward_addtime": {"type": "integer"},
  "reward_addmoney": {"type": "float"},
  "reward_info": {"type": "string"},
  "force_register_cs": {"type": "boolean"},
  "force_dedicated_ba": {"type": "boolean"},
  "coupon_group": {"type": "string"},
  "coupon_group_secondary": {"type": "string"},
  "tariff_name": {"type": "string"},
  "tariff_related_model": {"type": "string"},
  "tariff_type": {"type": "string"},
  "tariff_quantity": {"type": "string"},
  "maintenance_reservation_type": {"type": "string"}, # selection
  "maintenance_forgive_reservation": {"type": "boolean"},
  "maintenance_type": {"type": "string"}, # selection
  "maintenance_duration": {"type": "string"},
  "maintenance_observations": {"type": "string"},
  "maintenance_carconfig_index": {"type": "string"},
  "maintenance_carconfig_home": {"type": "string"},
  "maintenance_cs_person_index": {"type": "string"},
  "maintenance_reservation_start": {"type": "string"},
  "maintenance_car_plate": {"type": "string"},
  "maintenance_create_car_service": {"type": "boolean"},
  "maintenance_car_service": {"type": "string"},
  "maintenance_discount_reservation": {"type": "boolean"},
  "data_partner_creation_type": {"type": "string", "required": True}, # selection
  "data_partner_cs_user_type": {"type": "string"}, # selection
  "data_partner_firstname": {"type": "string"},
  "data_partner_lastname": {"type": "string"},
  "data_partner_vat": {"type": "string"},
  "data_partner_email": {"type": "string"},
  "data_partner_mobile": {"type": "string"},
  "data_partner_phone": {"type": "string"},
  "data_partner_gender": {"type": "string"}, # selection
  "data_partner_birthdate_date": {
    "type": "string", 
    "regex": "\\d{4}-[01]\\d-[0-3]\\d"
  },
  "data_partner_street": {"type": "string"},
  "data_partner_zip": {"type": "string"},
  "data_partner_state": {"type": "string"},
  "data_partner_city": {"type": "string"},
  "data_partner_iban": {"type": "string"},
  "data_partner_driving_license_expiration_date": {
    "type": "string",
    "regex": "\\d{4}-[01]\\d-[0-3]\\d"
    },
  "data_partner_image_dni": {"type": "string"},
  "data_partner_image_driving_license": {"type": "string"},
  "external_obj_id": {"type": "integer"},
  "external_promo_obj_id": {"type": "integer"}
}

S_SM_REWARD_UPDATE = {
  "name": {"type": "string"},
  "reward_type": {"type": "string"}, # selection
  "promo_code": {"type": "string"},
  "related_analytic_account": {"type": "string"},
  "reward_date": {"type": "string", "regex": "\\d{4}-[01]\\d-[0-3]\\d"},
  "reward_addtime": {"type": "integer"},
  "reward_addmoney": {"type": "float"},
  "reward_info": {"type": "string"},
  "force_register_cs": {"type": "boolean"},
  "force_dedicated_ba": {"type": "boolean"},
  "coupon_group": {"type": "string"},
  "coupon_group_secondary": {"type": "string"},
  "tariff_name": {"type": "string"},
  "tariff_related_model": {"type": "string"},
  "tariff_type": {"type": "string"},
  "tariff_quantity": {"type": "string"},
  "maintenance_reservation_type": {"type": "string"}, # selection
  "maintenance_forgive_reservation": {"type": "boolean"},
  "maintenance_type": {"type": "string"}, # selection
  "maintenance_duration": {"type": "string"},
  "maintenance_observations": {"type": "string"},
  "maintenance_carconfig_index": {"type": "string"},
  "maintenance_carconfig_home": {"type": "string"},
  "maintenance_cs_person_index": {"type": "string"},
  "maintenance_reservation_start": {"type": "string"},
  "maintenance_car_plate": {"type": "string"},
  "maintenance_create_car_service": {"type": "boolean"},
  "maintenance_car_service": {"type": "integer"},
  "maintenance_discount_reservation": {"type": "boolean"},
  "data_partner_creation_type": {"type": "string"}, # selection
  "data_partner_cs_user_type": {"type": "string"}, # selection
  "data_partner_firstname": {"type": "string"},
  "data_partner_lastname": {"type": "string"},
  "data_partner_vat": {"type": "string"},
  "data_partner_email": {"type": "string"},
  "data_partner_mobile": {"type": "string"},
  "data_partner_phone": {"type": "string"},
  "data_partner_gender": {"type": "string"}, # selection
  "data_partner_birthdate_date": {
    "type": "string", 
    "regex": "\\d{4}-[01]\\d-[0-3]\\d"
  },
  "data_partner_street": {"type": "string"},
  "data_partner_zip": {"type": "string"},
  "data_partner_state": {"type": "integer"},
  "data_partner_city": {"type": "string"},
  "data_partner_iban": {"type": "string"},
  "data_partner_driving_license_expiration_date": {
    "type": "string",
    "regex": "\\d{4}-[01]\\d-[0-3]\\d"
    },
  "data_partner_image_dni": {"type": "string"},
  "data_partner_image_driving_license": {"type": "string"},
  "external_obj_id": {"type": "integer"},
  "external_promo_obj_id": {"type": "integer"}
}

S_SM_REWARD_VALIDATE = {"_id": {"type": "integer"}}
