from ..database import db, Model , Column
from ..extensions import marshmallow

from marshmallow import post_dump

from sqlalchemy.orm import validates
from sqlalchemy_utils import Timestamp

import pycountry


class UserInformation(Model, Timestamp):
  __tablename__ = 'user_information'
  id      = Column(db.Integer, primary_key=True)
  id_user = Column(db.Integer, db.ForeignKey('user.id'))
  country = Column(db.String(100), nullable=True)
  bio     = Column(db.String(156), default="None", nullable=True)
  
  @validates('country')
  def validate_if_country_exist(self, key, country):
    import pycountry
    searched = [x for x in pycountry.countries if x.name.lower() == country.lower()]
    assert len(searched) == 1
    return searched[0].alpha_2

  def __init__(self, id_user, country=None, bio=None):
    self.id_user = id_user
    self.country = country
    self.bio     = bio


class UserInformationSchema(marshmallow.Schema):      
  class Meta:
    fields = ('country', 'bio')

  @post_dump
  def country_alpha_2_to_name(self, in_data):
    """ Transform country alpha_2 to country name """
    in_data['country'] = [x.name for x in pycountry.countries if x.alpha_2 == in_data['country']][0].capitalize()
    return in_data