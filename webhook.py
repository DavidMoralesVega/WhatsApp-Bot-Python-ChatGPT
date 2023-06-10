from flask import jsonify, request

class WebhookHandler:
    def __init__(self, verify_token):
        self.verify_token = verify_token

    def handle_request(self):
        if request.method == "GET":
            return self.handle_verification()
        elif request.method == "POST":
            return self.handle_message()

    def handle_verification(self):
        if request.args.get('hub.verify_token') == self.verify_token:
            return request.args.get('hub.challenge')
        else:
            return "Error de autentificacion."

    def handle_message(self):
        data = request.get_json()
        telefonoCliente = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        idWA = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
        timestamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']

        if mensaje is not None:
            respuesta = self.generate_response(mensaje)
            self.send(telefonoCliente, respuesta)

        return jsonify({"status": "success"}), 200

    def generate_response(self, mensaje):
        import openai
        openai.api_key = "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"
        model_engine = "text-davinci-003"
        prompt = mensaje
        completion = openai.Completion.create(engine=model_engine,
                                            prompt=prompt,
                                            max_tokens=1024,
                                            n=1,
                                            stop=None,
                                            temperature=0.7)
        respuesta = ""
        for choice in completion.choices:
            respuesta += choice.text

        respuesta = respuesta.replace("\\n", "\\\n")
        respuesta = respuesta.replace("\\", "")
        return respuesta

    def send(self, telefonoRecibe, respuesta):
        from heyoo import WhatsApp
        token = 'EAALXvDnen58BAO2g1AqzHvOWFYlz6nVo39fLrqfp8GDfMSLLWF3ONp7iX7OvSbgQsBocOMqseaBqrz5vngBuN1zcLTZA7jI5EaQ5vCUlw3OXCIPkHFRo9EjuvS3a5ZAXAD5aP1MrJOYRHdO4oMhxbVS8pby8ak2sAkrATUXWkcePb2k5lWRL77vNIMw2u0WDaZCn8psyglLxbZB1UZCqHcjcizJ2ZCAAAZD'
        idNumeroTeléfono = '102870155792565'
        mensajeWa = WhatsApp(token, idNumeroTeléfono)
        telefonoRecibe = telefonoRecibe.replace("521", "52")
        mensajeWa.send_message(respuesta, telefonoRecibe)
