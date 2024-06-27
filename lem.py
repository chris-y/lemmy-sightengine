#!/usr/bin/python3
from pythorhead import Lemmy

def login(instance, user, pw):
  lemmy = Lemmy(f'https://{instance}', raise_exceptions=True)
  try:
    lemmy.log_in(user, pw)
  except Exception as e:
    print(f'login failed: {e}\n')
    return None

  return lemmy
