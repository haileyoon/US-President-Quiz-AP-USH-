from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

presidents = [
    (1, "George", "Washington", "1789", "1797", "Independent"),
    (2, "John", "Adams", "1797", "1801", "Federalist"),
    (3, "Thomas", "Jefferson", "1801", "1809", "Democratic-Republican"),
    (4, "James", "Madison", "1809", "1817", "Democratic-Republican"),
    (5, "James", "Monroe", "1817", "1825", "Democratic-Republican"),
    (6, "John Quincy", "Adams", "1825", "1829", "Democratic-Republican"),
    (7, "Andrew", "Jackson", "1829", "1837", "Democratic"),
    (8, "Martin", "Van Buren", "1837", "1841", "Democratic"),
    (9, "William", "Harrison", "1841", "1841", "Whig"),
    (10, "John", "Tyler", "1841", "1845", "Whig"),
    (11, "James", "Polk", "1845", "1849", "Democratic"),
    (12, "Zachary", "Taylor", "1849", "1850", "Whig"),
    (13, "Millard", "Fillmore", "1850", "1853", "Whig"),
    (14, "Franklin", "Pierce", "1853", "1857", "Democratic"),
    (15, "James", "Buchanan", "1857", "1861", "Democratic"),
    (16, "Abraham", "Lincoln", "1861", "1865", "Republican"),
    (17, "Andrew", "Johnson", "1865", "1869", "National Union"),
    (18, "Ulysses", "Grant", "1869", "1877", "Republican"),
    (19, "Rutherford", "Hayes", "1877", "1881", "Republican"),
    (20, "James", "Garfield", "1881", "1881", "Republican"),
    (21, "Chester", "Arthur", "1881", "1885", "Republican"),
    (22, "Grover", "Cleveland", "1885", "1889", "Democratic"),
    (23, "Benjamin", "Harrison", "1889", "1893", "Republican"),
    (24, "Grover", "Cleveland", "1893", "1897", "Democratic"),
    (25, "William", "McKinley", "1897", "1901", "Republican"),
    (26, "Theodore", "Roosevelt", "1901", "1909", "Republican"),
    (27, "William", "Taft", "1909", "1913", "Republican"),
    (28, "Woodrow", "Wilson", "1913", "1921", "Democratic"),
    (29, "Warren", "Harding", "1921", "1923", "Republican"),
    (30, "Calvin", "Coolidge", "1923", "1929", "Republican"),
    (31, "Herbert", "Hoover", "1929", "1933", "Republican"),
    (32, "Franklin", "Roosevelt", "1933", "1945", "Democratic"),
    (33, "Harry", "Truman", "1945", "1953", "Democratic"),
    (34, "Dwight", "Eisenhower", "1953", "1961", "Republican"),
    (35, "John", "Kennedy", "1961", "1963", "Democratic"),
    (36, "Lyndon", "Johnson", "1963", "1969", "Democratic"),
    (37, "Richard", "Nixon", "1969", "1974", "Republican"),
    (38, "Gerald", "Ford", "1974", "1977", "Republican"),
    (39, "Jimmy", "Carter", "1977", "1981", "Democratic"),
    (40, "Ronald", "Reagan", "1981", "1989", "Republican"),
    (41, "George H W", "Bush", "1989", "1993", "Republican"),
    (42, "Bill", "Clinton", "1993", "2001", "Democratic"),
    (43, "George W", "Bush", "2001", "2009", "Republican"),
    (44, "Barack", "Obama", "2009", "2017", "Democratic"),
    (45, "Donald", "Trump", "2017", "2021", "Republican"),
    (46, "Joe", "Biden", "2021", "2025", "Democratic"),
    (47, "Donald", "Trump", "2025", "2029", "Republican")
]

correct_answers = {}
original_names = {}
def normalize_name(s):
    return s.lower().strip().replace('.', '').replace('  ', ' ')


def normalize_year(s):
    return s.strip()


for p in presidents:
    num, first, last, start, end, party = p

    correct_answers[num] = {
        'first': normalize_name(first),
        'last': normalize_name(last),
        'start': start.strip(),
        'end': end.strip(),
        'party': normalize_name(party)
    }

    original_names[num] = {
        'first': first,
        'last': last,
        'start': start,
        'end': end,
        'party': party
    }

@app.route('/')
def index():
    return render_template('index.html', presidents=presidents)


@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    num = int(data.get('num'))
    field = data.get('field')
    user_input = data.get('value', '')
    if num not in correct_answers:
        print(f"Invalid num: {num}")
        return jsonify({'valid': False})
    expected = correct_answers[num][field]
    if field in ['start', 'end']:
        user_norm = normalize_year(user_input)
    else:
        user_norm = normalize_name(user_input)
    print(f"Comparing user_norm: '{user_norm}' with expected: '{expected}'"
          )  # Debug
    is_valid = user_norm == expected
    print(f"Validation result: {is_valid}")
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
            'party': answers['party']
        })
    return jsonify({'error': 'No answer available'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
