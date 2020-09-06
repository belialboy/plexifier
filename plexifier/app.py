import json
import logging
import requests
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getBoundary(event):
    """
    This function grabs the boundary in the HTTP webhook call for the form data
    """
    
    return (event['headers']['Content-Type'].replace("multipart/form-data; boundary=",""))

def getBody(event):
    """
    This function grabs the body of th webhook data, and returns the result as a json object
    """
    
    boundary = getBoundary(event)
    components = event['body'].split(boundary)
    jsonStr = components[1].split("Content-Type: application/json",1)[1].replace("--']","").replace("--","")
    jsonBody = json.loads(jsonStr)
    return jsonBody
    
def sendToPushbullet(title,text):
    """
    This function sends a notice to Pushbullet
    """
    
    uri = "https://api.pushbullet.com/v2/pushes"
    reply = requests.post(uri,headers={'Access-Token': 'o.DxvRNu26B2qdy0cI3mm1BNycsmq5jaDg'},data={"body":text,"title":title,"type":"note"})
    logger.debug(reply)
    
def getTitleAsString(meta):
    """
    This function creates a title for the media that's been interacted with, and returns a single simple string
    """
    
    if "episode" in meta['type']:
        if "title" in meta:
            return "{PROGRAMME} - {SEASON} Episode {EPISODE} \"{TITLE}\"".format(PROGRAMME=meta['grandparentTitle'],SEASON=meta['parentTile'],EPISODE=meta['index'],TITLE=meta['title'])
        else:
            return "{PROGRAMME} - {SEASON} Episode {EPISODE}".format(PROGRAMME=meta['grandparentTitle'],SEASON=meta['parentTile'],EPISODE=meta['index'])
    else:
        return meta['title']
    
def lambda_handler(event, context):
    logger.setLevel(logging.DEBUG)
    logger.info(event)
    body = getBody(event)
    logger.debug(body)

    # filter on body['event'] = "media.stop", etc
    if body['user'] and body['owner']:
        if "library.new" in body['event']:
            # Send a notification to me via push bullet
            logger.info("Sending Pushbullet")
            sendToPushbullet("New Content",getTitleAsString(body['Metadata']))
            logger.info("Done")
        elif "media.scrobble" in body['event']:
            # Tweet about it
            logger.info("Sending Pushbullet")
            sendToPushbullet(body['Title'],"You just watched this video")
            logger.info("Done")
    
    return {
        'statusCode': 200,
        'body': "OK"
    }
