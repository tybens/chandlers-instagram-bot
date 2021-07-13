import os
import json

from bot import main, login


def lambda_handler(event, context):
    TOTAL_POSTS = 10  # max 25 I think
    cl = login(production=True)
    main(cl, TOTAL_POSTS)
    return {
        'statusCode': 200,
        'body': json.dumps('example')
    }
