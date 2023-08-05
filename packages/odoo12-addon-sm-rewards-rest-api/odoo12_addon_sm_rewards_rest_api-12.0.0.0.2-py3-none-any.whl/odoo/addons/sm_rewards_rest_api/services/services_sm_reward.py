import logging

from werkzeug.exceptions import BadRequest, NotFound

from odoo import _
from odoo.fields import Date

from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import Component

from . import schemas
from odoo.addons.sm_maintenance.models.models_api_services_utils import api_services_utils

_logger = logging.getLogger(__name__)

class SMRewardService(Component):
  _inherit = "emc.rest.service"
  _name = "sm_rewards.sm_reward.services"
  _usage = "sm-reward"
  _description = """
    SM Reward Service
  """

  def get(self, _id):
    record = self.env["sm_rewards.sm_reward"].search(
      [("id", "=", _id)]
    )
    if record:
      return self._to_dict(record)
    else:
      raise wrapJsonException(
        NotFound(_("No reward record for id %s") % _id)
      )

  def create(self, **params):  # pylint: disable=method-required-super
    params = self._prepare_create(params)
    record = self.env["sm_rewards.sm_reward"].create(params)
    return self._to_dict(record)

  def update(self, _id, **params):
    params = self._prepare_create(params)
    record = self.env["sm_rewards.sm_reward"].search(
      [("_api_external_id", "=", _id)]
    )
    if not record:
      raise wrapJsonException(
        NotFound(_("No update data record for id %s") % _id)
      )
    record.write(params)
    return self._to_dict(record)

  def validate(self, _id, **params):
    record = self.env["sm_rewards.sm_reward"].search(
      [("_api_external_id", "=", _id)]
    )
    if not record:
      raise wrapJsonException(
        NotFound(_("No reward record for id %s") % _id)
      )
    return self._to_dict(record)

  """Prepare a writable dictionary of values"""
  def _prepare_create(self, params):
    utils = api_services_utils.get_instance()
    attributes = self._get_attributes_list()
    create_dict = utils.generate_create_dictionary(params,attributes)
    create_dict['related_analytic_account_id'] = self._get_acc_id_from_params(params)
    create_dict['data_partner_state_id'] = self._get_state_id_from_params(params)
    create_dict['maintenance_car_service_id'] = self._get_carservice_id_from_params(params)
    return create_dict

  def _to_dict(self, record):
    record.ensure_one()
    utils = api_services_utils.get_instance()
    attributes = self._get_attributes_list()
    attributes.append('state')
    attributes.append('final_state')
    rel_attributes = {
      "related_analytic_account_id" : "name",
      "maintenance_car_service_id": "name",
      "data_partner_state_id": "code"
    }
    return utils.generate_get_dictionary(record,attributes,rel_attributes)

  def _get_acc_id_from_params(self,params):
    try:
      query_value = params['related_analytic_account']
    except:
      query_value = False
    if query_value:
      acc_id = self.env['account.analytic.account'].search([('name','=',query_value)]).id
      if not acc_id:
        raise wrapJsonException(
          BadRequest(
            'Analytic account %s not found' % (query_value)
          ),
          include_description=True,
        )
      return acc_id
    return False

  def _get_state_id_from_params(self,params):
    try:
      query_value = params['data_partner_state']
    except:
      query_value = False
    if query_value:
      company = self.env.user.company_id
      if company.country_id:
        state_id = self.env['res.country.state'].search([
          ('code', '=', query_value),
          ('country_id', '=', company.country_id.id),
        ]).id
        if not state_id:
          raise wrapJsonException(
            BadRequest(
              'State %s not found' % (query_value)
            ),
            include_description=True,
          )
        return state_id
    return False

  def _get_carservice_id_from_params(self,params):
    try:
      query_value = params['maintenance_car_service']
    except:
      query_value = False
    if query_value:
      cs_id = self.env['fleet.service.type'].search([('name','=',query_value)]).id
      if not cs_id:
        raise wrapJsonException(
          BadRequest(
            'Analytic account %s not found' % (query_value)
          ),
          include_description=True,
        )
      return cs_id
    return False

  def _validator_get(self):
    return schemas.S_SM_REWARD_GET

  def _validator_return_get(self):
    return schemas.S_SM_REWARD_RETURN_GET

  def _validator_create(self):
    return schemas.S_SM_REWARD_CREATE

  def _validator_return_create(self):
    return schemas.S_SM_REWARD_RETURN_GET

  def _validator_update(self):
    return schemas.S_SM_REWARD_UPDATE

  def _validator_return_update(self):
    return schemas.S_SM_REWARD_RETURN_GET

  def _validator_validate(self):
    return schemas.S_SM_REWARD_VALIDATE

  def _validator_return_validate(self):
    return schemas.S_SM_REWARD_RETURN_GET
  
  def _get_attributes_list(self):
    return [
      "name",
      "reward_type",
      "promo_code",
      "reward_date",
      "reward_addtime",
      "reward_addmoney",
      "reward_info",
      "force_register_cs",
      "force_dedicated_ba",
      "coupon_group",
      "coupon_group_secondary",
      "tariff_name",
      "tariff_related_model",
      "tariff_type",
      "tariff_quantity",
      "maintenance_reservation_type",
      "maintenance_forgive_reservation",
      "maintenance_type",
      "maintenance_duration",
      "maintenance_observations",
      "maintenance_carconfig_index",
      "maintenance_carconfig_home",
      "maintenance_cs_person_index",
      "maintenance_reservation_start",
      "maintenance_car_plate",
      "maintenance_create_car_service",
      "maintenance_discount_reservation",
      "data_partner_creation_type",
      "data_partner_cs_user_type",
      "data_partner_firstname",
      "data_partner_lastname",
      "data_partner_vat",
      "data_partner_email",
      "data_partner_mobile",
      "data_partner_phone",
      "data_partner_gender",
      "data_partner_birthdate_date",
      "data_partner_street",
      "data_partner_zip",
      "data_partner_city",
      "data_partner_iban",
      "data_partner_driving_license_expiration_date",
      "data_partner_image_dni",
      "data_partner_image_driving_license",
      "external_obj_id",
      "external_promo_obj_id"
    ]