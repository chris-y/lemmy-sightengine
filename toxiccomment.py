#!/usr/bin/python3

import requests
import json
import sys
import string
import firestore
from pythorhead import Lemmy
from pythorhead.types import SortType,ListingType

def run(lemmy, api_user, api_secret, live):
  examined_urls = None

  # add additional communities here and uncomment +ccomments below
  #
  #cid = lemmy.discover_community("imaginaryfairies@lemmings.world")
  #
  #try:
  #  ccomments = lemmy.comment.list(cid, sort=SortType.New, limit=10)
  #except Exception as e:
  #  print(f'cannot get comments: {e}\n')
  #  sys.exit(1)

  try:
    mcomments = lemmy.comment.list(sort=SortType.New, type_=ListingType.ModeratorView, limit=10)
  except Exception as e:
    print(f'cannot get moderator comments: {e}\n')

  comments = mcomments #+ ccomments

  for c in comments:
    print(c['comment']['content'])

    if c['saved'] is True:
      break

    data = {
      'text': c['comment']['content'],
      'mode': 'ml',
      'lang': 'en',
      'models': 'general',
      'api_user': api_user,
      'api_secret': api_secret
    }
    r = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)

    output = json.loads(r.text)

    if output['status'] == "success":
      flag = False
      report = ""
      for mc in output['moderation_classes']['available']:
        report += f'{mc}: {output["moderation_classes"][mc]}\n'
        if output['moderation_classes'][mc] > 0.8:
          flag = True
      print(report)

      if live:
        if flag is True:
          try:
            lemmy.report(c["comment"]["id"], f'Flagged as:\n{report}')
            lemmy.comment.save(c['comment']['id'], True)
          except Exception as e:
            print("unable to raise report: {e}")
            continue

        # save the comment so we don't process it again
        # should proably mark as read but that doesn't work
        try:
          lemmy.comment.save(c['comment']['id'], True)
        except Exception as e:
          print("unable to save comment: {e}")
          continue
