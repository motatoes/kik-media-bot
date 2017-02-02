from flask import Flask, request, Response

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

try:
    from settings import *
except ImportError:
    from settings.example import *

app = Flask(__name__)
kik = KikApi(BOT_USERNAME, BOT_API_KEY)

kik.set_configuration(Configuration(webhook=WEBHOOK))

@app.route('/webhook', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, TextMessage):
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body
                )
            ])

    return Response(status=200)


if __name__ == "__main__":
    app.run(port=8080, debug=True)