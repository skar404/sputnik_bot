# sputnik_bot
[![Build Status](https://cloud.drone.io/api/badges/skar404/sputnik_bot/status.svg)](https://cloud.drone.io/skar404/sputnik_bot)
[![codecov](https://codecov.io/gh/skar404/sputnik_bot/branch/master/graph/badge.svg)](https://codecov.io/gh/skar404/sputnik_bot)

Auto post new to weibo and telegram 

---
run: 
```bash
pip install -r requirements.txt
python manage.py api # run web server (post news to weibo)
python manage.py schedule # run schedule (get new post and send to telegram)
```
