from ..extensions import marshmallow

from marshmallow import post_dump

import pycountry


class UserInformationSchema(marshmallow.Schema):      
  class Meta:
    fields = ('country', 'bio')

  @post_dump
  def country_alpha_2_to_name(self, in_data):
    """ Transform country alpha_2 to country name """
    in_data['country'] = [x.name for x in pycountry.countries if x.alpha_2 == in_data['country']][0].capitalize()
    return in_data