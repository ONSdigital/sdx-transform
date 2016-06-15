import settings
import json
import logging
import logging.handlers
from io import BytesIO
from jinja2 import Environment, PackageLoader
from flask import Flask, request, make_response, send_file
from pcktransformer import derive_answers, form_ids
from PDFTransformer import PDFTransformer
from ImageTransformer import ImageTransformer

import dateutil.parser

env = Environment(loader=PackageLoader('transform', 'templates'))

app = Flask(__name__)

app.config['WRITE_BATCH_HEADER'] = settings.WRITE_BATCH_HEADER


test_message = '''{
   "type": "uk.gov.ons.edc.eq:surveyresponse",
   "origin": "uk.gov.ons.edc.eq",
   "survey_id": "023",
   "version": "0.0.1",
   "collection": {
     "exercise_sid": "hfjdskf",
     "instrument_id": "0203",
     "period": "0216"
   },
   "submitted_at": "2016-03-12T10:39:40Z",
   "metadata": {
     "user_id": "789473423",
     "ru_ref": "12345678901A"
   },
   "data": {
     "11": "01/04/2016",
     "12": "31/10/2016",
     "20": "1800000",
     "51": "84",
     "52": "10",
     "53": "73",
     "54": "24",
     "50": "205",
     "22": "705000",
     "23": "900",
     "24": "74",
     "25": "50",
     "26": "100",
     "21": "60000",
     "27": "7400",
     "146": "some comment"
   }
}'''


@app.route('/pck', methods=['POST'])
@app.route('/pck/<batch_number>', methods=['POST'])
def render_pck(batch_number=30001):
    batch_number = int(batch_number)
    response = request.get_json(force=True)
    template = env.get_template('pck.tmpl')

    form_id = response['collection']['instrument_id']

    instrument_id = response['collection']['instrument_id']

    submission_date = dateutil.parser.parse(response['submitted_at'])
    submission_date_str = submission_date.strftime("%d/%m/%y")

    cs_form_id = form_ids[instrument_id]

    data = response['data'] if 'data' in response else {}

    with open("./surveys/%s.%s.json" % (response['survey_id'], form_id)) as json_file:
        survey = json.load(json_file)

        answers = derive_answers(survey, data)

        return template.render(response=response, submission_date=submission_date_str,
                               batch_number=batch_number, form_id=cs_form_id,
                               answers=answers, write_batch_header=app.config['WRITE_BATCH_HEADER'])


@app.route('/idbr', methods=['POST'])
def render_idbr():
    response = request.get_json(force=True)
    template = env.get_template('idbr.tmpl')

    return template.render(response=response)


@app.route('/html', methods=['POST'])
def render_html():
    response = request.get_json(force=True)
    template = env.get_template('html.tmpl')

    form_id = response['collection']['instrument_id']

    with open("./surveys/%s.%s.json" % (response['survey_id'], form_id)) as json_file:
        survey = json.load(json_file)
        return template.render(response=response, survey=survey)


@app.route('/pdf', methods=['POST'])
def render_pdf():
    survey_response = request.get_json(force=True)

    form_id = survey_response['collection']['instrument_id']

    with open("./surveys/%s.%s.json" % (survey_response['survey_id'], form_id)) as json_file:
        survey = json.load(json_file)
        buffer = BytesIO()
        pdf = PDFTransformer(buffer, survey, survey_response)
        rendered_pdf = pdf.render()

        response = make_response(rendered_pdf)
        # response.headers['Content-Disposition'] = "attachment; filename='response.pdf"
        response.mimetype = 'application/pdf'

        return response


@app.route('/images', methods=['POST'])
def render_images():
    pass


@app.route('/image-test', methods=['GET'])
def image_test():
    survey_response = json.loads(test_message)
    form_id = survey_response['collection']['instrument_id']

    with open("./surveys/%s.%s.json" % (survey_response['survey_id'], form_id)) as json_file:
        survey = json.load(json_file)
        image_transformer = ImageTransformer(survey, survey_response)
        
        zipname = image_transformer.create_image_zip()

        image_transformer.cleanup()

        return send_file(zipname, mimetype='application/zip')

@app.route('/pdf-test', methods=['GET'])
def pdf_test():
    survey_response = json.loads(test_message)
    form_id = survey_response['collection']['instrument_id']

    with open("./surveys/%s.%s.json" % (survey_response['survey_id'], form_id)) as json_file:
        survey = json.load(json_file)
        buffer = BytesIO()
        pdf = PDFTransformer(survey, survey_response)
        rendered_pdf = pdf.render(buffer)

        response = make_response(rendered_pdf)
        # response.headers['Content-Disposition'] = "attachment; filename='response.pdf"
        response.mimetype = 'application/pdf'

        return response


@app.route('/html-test', methods=['GET'])
def html_test():

    response = json.loads(test_message)
    template = env.get_template('html.tmpl')
    form_id = response['collection']['instrument_id']

    with open("./surveys/%s.%s.json" % (response['survey_id'], form_id)) as json_file:
        survey = json.load(json_file)
        return template.render(response=response, survey=survey)

if __name__ == '__main__':
    # Startup
    logging.basicConfig(level=settings.LOGGING_LEVEL, format=settings.LOGGING_FORMAT)
    app.run(debug=True, host='0.0.0.0')
