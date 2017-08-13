from flask import Flask, render_template, redirect, request, session
import csv

app = Flask(__name__)


def open_csv(filename='records.csv'):  # Opens the csv file and creates a list of lists from it.
    records = []
    with open(filename, 'r') as open_csv:
        saved_records = csv.reader(open_csv)
        for record in saved_records:
            records.append(record)
    return records


def save_to_csv(table, filename='records.csv'):  # Updates the csv file with the table of data in the argument.
    with open(filename, 'w', newline='') as open_csv:
        writer = csv.writer(open_csv)
        writer.writerows(table)
    return table


def last_id(table):
    if len(table) > 0:
        return int(table[-1][0]) + 1
    return 1

@app.route('/')  # Displayes the list from the opened csv file.
def route_list():
    return render_template('list.html', records=open_csv())


@app.route('/story', methods=['GET', 'POST'])
@app.route('/story/<_id>', methods=['GET', 'POST'])
def route_form(_id=None):
    table = open_csv()
    story_to_update = []
    for story in table:
        if story[0] == _id:
            _id = story[0]
            story_to_update = story
    return render_template('form.html', story=story_to_update, _id=_id)


@app.route('/save-story', methods=['GET', 'POST'])
def route_save():
    table = open_csv()
    new_story = []
    new_story.append(last_id(table))
    new_story.append(request.form['story_title'])
    new_story.append(request.form['user_story'])
    new_story.append(request.form['criteria'])
    new_story.append(request.form['value'])
    new_story.append(request.form['estimation'])
    new_story.append(request.form['status'])
    table.append(new_story)
    save_to_csv(table)
    return redirect('/')


@app.route('/story/update-story/<_id>', methods=['GET', 'POST'])
def route_update(_id):
    table = open_csv()
    for record in table:
        if record[0] == _id:
            record[1] = request.form['story_title']
            record[2] = request.form['user_story']
            record[3] = request.form['criteria']
            record[4] = request.form['value']
            record[5] = request.form['estimation']
            record[6] = request.form['status']
    save_to_csv(table)
    return redirect('/')


@app.route('/remove-story/<_id>', methods=['GET'])
def route_remove(_id):
    new_table = []
    table = open_csv()
    for record in table:
        if record[0] != _id:
            new_table.append(record)
    save_to_csv(new_table)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
