import re

import requests
from django.conf import settings

from computrabajo_bot.celery import app
from computrabajo_bot.utils import catch_exceptions, ComputrabajoStatusCodeError


def validate_200(res) -> None:
    """
    raise IOError if status_code != 200
    """
    if res.status_code != 200:
        raise ComputrabajoStatusCodeError('Received status_code=[%d] from url=[%s]' % (res.status_code, res.url))


def send_email(email, text):
    """
    sends an email using mailgun api with the task results
    :return:
    """
    data = {
        "from": "Excited User <mailgun@%s>" % settings.MAILGUN_DOMAIN,
        "to": [email],
        "subject": "Resultados Computrabajo Bot",
        "text": text
    }
    url = "https://api.mailgun.net/v3/%s/messages" % settings.MAILGUN_DOMAIN
    requests.post(url, auth=("api", settings.MAILGUN_PRIV_API_KEY), data=data)


@app.task
@catch_exceptions
def process_request(data) -> None:
    """
    login using computrabajo creds, query for positions and apply the request user to all of them
    """
    username = data['username']
    password = data['password']
    query = data.get('query')
    city = data.get('state')
    salary = data.get('salary')
    pub_date_delta = data.get('pub')
    post_regex = r"['\"]/ofertas-de-trabajo/[^'\"]+\-(\w+)"

    # urls
    login_url = 'https://www.computrabajo.com.mx/Ajax/checkLogin.ashx'
    search_url_template = 'https://www.computrabajo.com.mx/empleos-en-%s?q=%s'
    apply_url_template = 'https://candidato.computrabajo.com.mx/match/?oi=%s&p=47&idb=2'

    # messages
    success_msg = 'Te has postulado correctamente'
    already_done_msg = 'Ya te has postulado anteriormente'
    some_questions_msg = 'Responde a las siguientes preguntas'

    # login user
    s = requests.session()
    url = login_url
    data = {
        'pe': username,
        'pp': password,
        'rp': 0
    }
    res = s.post(url, data)
    validate_200(res)

    url_param = res.json().get('url')
    if not url_param:
        raise IOError('Url param missing from POST %s response' % url)

    res = s.get(url_param)
    validate_200(res)

    # search for jobs using query and params
    url = search_url_template % (city, query)
    params = {
        'pubdate': pub_date_delta,
        'q': query,
        'sal': salary
    }
    res = s.get(url, params=params)
    validate_200(res)

    post_codes = re.findall(post_regex, res.text)
    urls_need_form = []

    # post applications
    for pc in post_codes:
        url = apply_url_template % pc
        res = s.get(url)
        validate_200(res)

        if success_msg not in res.text and already_done_msg not in res.text:
            if some_questions_msg in res.text:
                urls_need_form.append(res.url)

            else:
                text = (
                    'Encontramos un problema mientras intentábamos postularte a todas las vacantes\n'
                    'Es probable que computrabajo haya detectado actividad inusual y te pida que resuelvas un captcha '
                    'para seguir postulándote.\n'
                    'Por favor aplica a esta vacante [%s] o a cualquier otra y vuelve a intentar correr el bot.'
                ) % res.url
                return send_email(username, text)

    if urls_need_form:
        text = (
            'Logramos postularte a la mayoría de las vacantes, pero una o más requieren que respondas un formulario '
            'hecho por la empresa. A continuación enlistamos los urls de con los formualrios para postularte: \n'
        )
        text += '\n'.join(urls_need_form)
        return send_email(username, text)

    text = (
        'Logramos postularte exitosamente a las vacantes. Puedes ver más información sobre tus postulaciones en tu '
        'perfil, siguiendo este url: %s'
    ) % settings.COMPUTRABAJO_PROFILE_URL
    send_email(username, text)