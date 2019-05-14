# sputnik_bot
[![Build Status](https://cloud.drone.io/api/badges/skar404/sputnik_bot/status.svg)](https://cloud.drone.io/skar404/sputnik_bot)
[![codecov](https://codecov.io/gh/skar404/sputnik_bot/branch/master/graph/badge.svg)](https://codecov.io/gh/skar404/sputnik_bot)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c2b02c7268974f668f7c96191e6ef606)](https://www.codacy.com/app/skar404/sputnik_bot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=skar404/sputnik_bot&amp;utm_campaign=Badge_Grade)

Auto post new to weibo and telegram 

---
run: 
```bash
pip install -r requirements.txt
python manage.py api # run web server (post news to weibo)
python manage.py schedule # run schedule (get new post and send to telegram)
```
