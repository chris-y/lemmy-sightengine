import sys
import os
import aireport
import toxiccomment
import lem

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)

BOTUSER = os.getenv("LEMMY_USER",0)
BOTPW = os.getenv("LEMMY_PW", 0)
BOTINSTANCE = os.getenv("LEMMY_INSTANCE", 0)
APIUSER = os.getenv("API_USER", 0)
APISECRET = os.getenv("API_SECRET", 0)

def main(user, pw, inst, apiuser, apisecret):

    lemmy = lem.login(inst, user, pw)
    if lemmy is None:
      sys.exit(1)

    aireport.run(lemmy, user, inst, apiuser, apisecret, True)
    toxiccomment.run(lemmy, apiuser, apisecret, True)
    return "aireportbot"

# Start script
if __name__ == "__main__":
    try:
        main(BOTUSER, BOTPW, BOTINSTANCE, APIUSER, APISECRET)
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(message)
        sys.exit(1)  # Retry Job Task by exiting the process
