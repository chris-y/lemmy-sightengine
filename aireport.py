#!/usr/bin/python3

import requests
import json
import sys
import string
import firestore
from pythorhead import Lemmy
from pythorhead.types import SortType,ListingType

def run(lemmy, user, instance, apiuser, apisecret, live):
  examined_urls = None
  posted_reports = { }
  posted_reports["posts"] = []
  posted_reports["comments"] = []
  doc = f'{user}.{instance}'
  if live:
    examined_urls = firestore.get("aireports", doc)
  if examined_urls is None:
    examined_urls = {}

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
      
    if "url" in p["post"]:
      if "url_content_type" in p["post"]:
        # confirm it is an image
        if p['post']['url_content_type'][:5] != 'image':
          continue

      if p["post"]["url"] in examined_urls:
        ''' this is cached already - don't re-submit '''
      else:
        params = {
          'url': p["post"]["url"],
          'models': 'genai',
          'api_user': apiuser,
          'api_secret': apisecret
        }

        r = requests.get('https://api.sightengine.com/1.0/check.json', params=params)
        output = json.loads(r.text)
        if output['status'] == "success":
          #print(f'{p["post"]["title"]}: {output["type"]["ai_generated"]}')
          examined_urls[p["post"]["url"]] = output["type"]["ai_generated"]
        else:
          continue

        if live:
          try:
            lemmy.post.mark_as_read(p["post"]["id"], True)
          except Exception as e:
            print(f'cannot mark as read: {e}\n')

      if live:
        if examined_urls[p["post"]["url"]] >= 0.5:
          try:
            lemmy.report(p["post"]["id"], f'Suspected AI {examined_urls[p["post"]["url"]]}') # raise report
          except Exception as e:
            print("unable to raise report: {e}")

  if live:
    firestore.set("aireports", doc, examined_urls)

  return lemmy
