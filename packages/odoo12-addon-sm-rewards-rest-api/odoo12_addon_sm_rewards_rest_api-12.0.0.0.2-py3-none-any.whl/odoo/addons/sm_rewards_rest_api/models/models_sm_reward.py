from odoo import models

class sm_reward(models.Model):
    _name = "sm_rewards.sm_reward"
    _inherit = ["sm_rewards.sm_reward", "external.id.mixin"]