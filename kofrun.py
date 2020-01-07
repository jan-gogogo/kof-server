# -*- coding: utf-8 -*
import datetime

from app import app
from app import views
from app import scheduler
import app.service.kof as KOF

if __name__ == '__main__':
    scheduler.add_job(func=KOF.battle_timer, id="battle", args=(),
                      run_date=datetime.datetime.now() + datetime.timedelta(seconds=2))
    app.run(host="0.0.0.0", port=8080, debug=False)
