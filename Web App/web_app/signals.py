from django.db.models.signals import post_migrate
from django.dispatch import receiver
from web_app.models import Mirror


@receiver(post_migrate)
def create_mirror_object(sender, **kwargs):
    """
        Ensures a single Mirror object with id=2 exists after migrations.
    """
    try:
        mirror = Mirror.objects.filter(mid=2).first()
        if mirror:
            Mirror.objects.exclude(mid=2).delete()
        else:
            Mirror.objects.create(mid=2, mirror_name="Default Mirror")
    except Exception as e:
        print(f"Error ensuring Mirror with id=2: {e}")