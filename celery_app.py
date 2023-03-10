from celery import Celery
from celery.schedules import crontab
from DB_dir.db_connection import DatabaseConnection
from SERVICE_dir.send_recovery_code import send_recovery_code
c_app = Celery(
    'celery_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1')

c_app.conf.enable_utc = False


@c_app.task
def change_tarif_if_expire():
    with DatabaseConnection.create_cursor() as cursor:
        try:
            cursor.execute("""update saved_order_and_tarif set order_state = false 
            where tarif_id_fk in
            (select c_t_tarif_id  from client_tarif ct 
            where end_license::date <= current_date);""")
            DatabaseConnection.commit()
        except Exception as e:
            print(e)
            raise e


c_app.conf.beat_schedule = {
    "birthday-task": {
        "task": "celery_app.change_tarif_if_expire",
        "schedule": crontab(hour=0, minute=0)
    }
}

