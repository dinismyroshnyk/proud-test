import asyncio
from aiosmtpd.controller import Controller

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from:', envelope.mail_from)
        print('Message for:', envelope.rcpt_tos)
        print('Message data:\n', envelope.content.decode())
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    controller = Controller(CustomSMTPHandler(), port=1025)
    controller.start()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()
