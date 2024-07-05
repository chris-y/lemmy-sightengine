#!/usr/bin/python3

import requests
import json
import sys
import string
import firestore
from pythorhead import Lemmy
from pythorhead.types import SortType,ListingType

def run(lemmy, live):
  threshold = -5 # posts below this score will be flagged

  # add additional communities here and uncomment the + cposts below
  #cid = lemmy.discover_community("imaginaryfairies@lemmings.world")
  #
  #try:
  #  cposts = lemmy.post.list(cid, sort=SortType.New, limit=10)
  #except Exception as e:
  #  print(f'cannot get posts: {e}\n')
  #  sys.exit(1)

  try:
    mposts = lemmy.post.list(sort=SortType.New, type_=ListingType.ModeratorView, limit=10)
  except Exception as e:
    print(f'cannot get moderator posts: {e}\n')

  posts = mposts #+ cposts

  for p in posts:
    if p["read"] is True:
      break

    if p['counts']['score'] < threshold:
      if live:
        try:
          lemmy.report(p["post"]["id"], f'Downvoted - Score {p["counts"]["score"]}') # raise report
        except Exception as e:
          print("unable to raise report: {e}")
          return
        try:
          lemmy.post.mark_as_read(p["post"]["id"], True)
        except Exception as e:
          print(f'cannot mark as read: {e}\n')

  return
