import string
import random
from flask import Flask, request, redirect

app = Flask(__name__)

# In-memory storage for URLs
url_mapping = {}
# Counter to generate unique IDs
counter = 1

# Characters used for creating short URLs (base62)
BASE62 = string.ascii_letters + string.digits

def encode(num):
    """Encodes a number into Base62 string."""
    if num == 0:
        return BASE62[0]
    result = []
    while num:
        num, rem = divmod(num, 62)
        result.append(BASE62[rem])
    return ''.join(reversed(result))

def decode(base62_str):
    """Decodes a Base62 string into a number."""
    num = 0
    for char in base62_str:
        num = num * 62 + BASE62.index(char)
    return num

@app.route('/shorten', methods=['POST'])
def shorten_url():
    global counter
    long_url = request.form['url']
    short_code = encode(counter)
    url_mapping[short_code] = long_url
    counter += 1
    return f'Short URL is: http://127.0.0.1:5000/{short_code}'

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
