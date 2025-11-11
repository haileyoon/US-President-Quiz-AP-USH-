from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

presidents = [(1, "George", "Washington", "1789", "1797"),
              (2, "John", "Adams", "1797", "1801"),
              (3, "Thomas", "Jefferson", "1801", "1809"),
              (4, "James", "Madison", "1809", "1817"),
              (5, "James", "Monroe", "1817", "1825"),
              (6, "John Quincy", "Adams", "1825", "1829"),
              (7, "Andrew", "Jackson", "1829", "1837"),
              (8, "Martin", "Van Buren", "1837", "1841"),
              (9, "William", "Harrison", "1841", "1841"),
              (10, "John", "Tyler", "1841", "1845"),
              (11, "James", "Polk", "1845", "1849"),
              (12, "Zachary", "Taylor", "1849", "1850"),
              (13, "Millard", "Fillmore", "1850", "1853"),
              (14, "Franklin", "Pierce", "1853", "1857"),
              (15, "James", "Buchanan", "1857", "1861"),
              (16, "Abraham", "Lincoln", "1861", "1865"),
              (17, "Andrew", "Johnson", "1865", "1869"),
              (18, "Ulysses", "Grant", "1869", "1877"),
              (19, "Rutherford", "Hayes", "1877", "1881"),
              (20, "James", "Garfield", "1881", "1881"),
              (21, "Chester", "Arthur", "1881", "1885"),
              (22, "Grover", "Cleveland", "1885", "1889"),
              (23, "Benjamin", "Harrison", "1889", "1893"),
              (24, "Grover", "Cleveland", "1893", "1897"),
              (25, "William", "McKinley", "1897", "1901"),
              (26, "Theodore", "Roosevelt", "1901", "1909"),
              (27, "William", "Taft", "1909", "1913"),
              (28, "Woodrow", "Wilson", "1913", "1921"),
              (29, "Warren", "Harding", "1921", "1923"),
              (30, "Calvin", "Coolidge", "1923", "1929"),
              (31, "Herbert", "Hoover", "1929", "1933"),
              (32, "Franklin", "Roosevelt", "1933", "1945"),
              (33, "Harry", "Truman", "1945", "1953"),
              (34, "Dwight", "Eisenhower", "1953", "1961"),
              (35, "John", "Kennedy", "1961", "1963"),
              (36, "Lyndon", "Johnson", "1963", "1969"),
              (37, "Richard", "Nixon", "1969", "1974"),
              (38, "Gerald", "Ford", "1974", "1977"),
              (39, "Jimmy", "Carter", "1977", "1981"),
              (40, "Ronald", "Reagan", "1981", "1989"),
              (41, "George H W", "Bush", "1989", "1993"),
              (42, "Bill", "Clinton", "1993", "2001"),
              (43, "George W", "Bush", "2001", "2009"),
              (44, "Barack", "Obama", "2009", "2017"),
              (45, "Donald", "Trump", "2017", "2021"),
              (46, "Joe", "Biden", "2021", "2025"),
              (47, "Donald", "Trump", "2025", "2029")]

correct_answers = {}
original_names = {}
for p in presidents:
    num, first, last, start, end = p
    correct_answers[num] = {
        'first': first.lower().strip().replace('.', ''),
        'last': last.lower().strip().replace('.', ''),
        'start': start.strip(),
        'end': end.strip()
    }
    original_names[num] = {
        'first': first,
        'last': last,
        'start': start,
        'end': end
    }


def normalize_name(s):
    return s.lower().strip().replace('.', '').replace('  ', ' ')


def normalize_year(s):
    return s.strip()


@app.route('/')
def index():
    return render_template('index.html', presidents=presidents)


@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    num = int(data.get('num'))  # Convert to int
    field = data.get('field')
    user_input = data.get('value', '')
    if num not in correct_answers:
        print(f"Invalid num: {num}")  # Debug
        return jsonify({'valid': False})
    expected = correct_answers[num][field]
    if field in ['start', 'end']:
        user_norm = normalize_year(user_input)
    else:
        user_norm = normalize_name(user_input)
    print(f"Comparing user_norm: '{user_norm}' with expected: '{expected}'"
          )  # Debug
    is_valid = user_norm == expected
    print(f"Validation result: {is_valid}")  # Debug
    return jsonify({'valid': is_valid})


@app.route('/answer/<int:num>', methods=['GET'])
def get_answer(num):
    if num in original_names:
        answers = original_names[num]
        return jsonify({
            'first': answers['first'],
            'last': answers['last'],
            'start': answers['start'],
            'end': answers['end']
        })
    return jsonify({'error': 'No answer available'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
