from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('59587272415374666370754C78676378787679334D6F487A7A596D5A536F7A474D6D574F507266786461513D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'{code} کد تایید شما'
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)