import pytest

from ...app.models import UserInformation


@pytest.mark.usefixtures('db')
class TestUser:
    """Test user information model"""

    def test_created_user_information_and_save_alpha_2_country(self, db, user):
      _user = user.get()
      db.session.commit()
      user_information = UserInformation(id_user=_user.id, country="Canada", bio="Sadness")
      db.session.add(user_information)
      db.session.commit()
      assert UserInformation.query.filter_by(country="Canada").first() == None
      assert UserInformation.query.filter_by(country="CA").first() != None
    
    def test_created_user_information_with_contry_that_does_not_exist(self, db, user):
      _user = user.get()
      db.session.commit()
      with pytest.raises(AssertionError):
        user_information = UserInformation(id_user=_user.id, country="Cannabis", bio="Sadness")

    def test_created_user_information_and_without_bio(self, db, user):
      _user = user.get()
      db.session.commit()
      user_information = UserInformation(id_user=_user.id, country="Canada")
      db.session.add(user_information)
      db.session.commit()
      assert user_information.bio == 'None'