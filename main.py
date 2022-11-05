from flask import Flask, render_template, request, flash, jsonify

import db

app = Flask(__name__)
app.secret_key = '3228'


@app.route('/')
def main_window():
    return render_template('Main_window.html')


@app.route('/about')
def about():
    model = request.args.get('model')
    template = 'Data_about_model_window.html' if not model else f'{model}.html'

    return render_template(template)


@app.route('/data')
def data():
    data_type = request.args.get('type')
    if not data_type in ('train', 'test', 'raw', 'prediction'):
        return render_template('Kust_Choice.html')

    db_data = db.get_data(data_type)
    if len(db_data) == 0:
        flash('Нет данных')
        return render_template('Kust_Choice.html')

    page_data = []
    if data_type in ('train', 'test'):
        for row in db_data:
            page_data.append(
                {
                    'Исходные данные': {'text': f'Куст {row["well_id"]} ({row["parameter"]})',
                                        'url': f'data_graph?data_type=raw&data_id={row["raw_data_id"]}'},
                    'Данные скорректированы': {'text': 'Да' if row['corrections'] else 'Нет'},
                    'Величина нормализации': {'text': row['normalization_value']},
                    'url': f'/data_graph?data_type={data_type}&data_id={row["id"]}'
                }
            )
    elif data_type == 'raw':
        for row in db_data:
            page_data.append(
                {
                    'Куст': {'text': row['well_id']},
                    'Параметр': {'text': row['parameter']},
                    'url': f'/data_graph?data_type={data_type}&data_id={row["id"]}'
                }
            )
    elif data_type == 'prediction':
        for row in db_data:
            page_data.append(
                {
                    'Тестовые данные':
                        {'text': f'Куст {row["well_id"]} ({row["parameter"]})',
                         'url': f'data_graph?data_type=test&data_id={row["test_data_id"]}',
                         'title': f'Данные{" не " if not row["test_data_corrections"] else " "}скорректированы, '
                                  f'величина нормализации: {row["normalization_value"]}'},
                    'Модель': {'text': row["network"]},
                    'url': f'/data_graph?data_type={data_type}&data_id={row["id"]}'
                }
            )
    if page_data:
        return render_template('data_choice.html', page_data=page_data)

    return render_template('Kust_Choice.html')


@app.route('/data_graph')
def get_data_graph():
    if 'data_type' in request.args and 'data_id' in request.args:
        return render_template('Data_graph_window.html',
                               data_type=request.args['data_type'], data_id=request.args['data_id'])
    return render_template('Data_graph_window.html')


@app.route('/data_values/<data_type>/<int:data_id>')
def get_data_values(data_type, data_id):
    if data_type not in ('train', 'test', 'raw', 'prediction'):
        return 'Wrong data_type', 400

    data_values = db.get_data_values(data_type, data_id)

    return jsonify(data_values)


@app.route('/ping')
def ping():
    return 'OK', 200


if __name__ == '__main__':
    app.run()
