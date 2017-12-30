import pytest, datetime

from ...app.models import Notification, NotificationSchema
from ..factories import UserFactory


@pytest.mark.usefixtures('db', 'user')
class TestNotification:
  """Test notification model"""

  def test_created_notification_and_relation_with_user(self, db, user):
    _user = user.get()
    db.session.commit()
    notification = Notification(id_user=_user.id, description="Carl answered your question",
                                status=u'unchecked', url="/questions/1")
    db.session.add(notification)
    db.session.commit()
    assert Notification.query.count() == 1
    notification = Notification.query.filter_by(id=1).first()
    assert notification.status.code == 'unchecked'
  
  def test_change_unchecked_to_checked(self, db, user):
    _user = user.get()
    db.session.commit()
    notification = Notification(id_user=_user.id, description="Carl answered your question",
                                status=u'unchecked', url="/questions/1")
    db.session.add(notification)
    db.session.commit()
    notification = Notification.query.filter_by(id=1).first()
    assert notification.status.code == 'unchecked'
    notification.status = u'checked'
    db.session.commit()
    assert notification.status.code == 'checked'

  def test_created_without_status(self, db, user):
    _user = user.get()
    db.session.commit()
    notification = Notification(id_user=_user.id, description="Carl answered your question",
                                url="/questions/1")
    db.session.add(notification)
    db.session.commit()
    notification = Notification.query.filter_by(id=1).first()
    assert notification.status.code == 'unchecked'

  def test_serialize_with_marshmallow(self, db, user):
    _user = user.get()
    db.session.commit()
    notification = Notification(id_user=_user.id, description="Carl answered your question",
                                url="/questions/1")
    db.session.add(notification)
    db.session.commit()
    notification_schema = NotificationSchema()
    notification_serialized = notification_schema.dump(notification).data
    assert notification_serialized['status'] == 'unchecked'
    assert notification_serialized['description'] == "Carl answered your question"
    assert notification_serialized['url'] == "/questions/1"

  def test_serialize_with_marshmallow_without_url(self, db, user):
    _user = user.get()
    db.session.commit()
    notification = Notification(id_user=_user.id, description="Carl answered your question")
    db.session.add(notification)
    db.session.commit()
    notification_schema = NotificationSchema()
    notification_serialized = notification_schema.dump(notification).data
    assert notification_serialized['status'] == 'unchecked'
    assert notification_serialized['description'] == "Carl answered your question"
    assert 'url' not in notification_serialized