from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Voucher(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    content = db.Column(db.String(200), nullable=True)
    price = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self):
        return '<Voucher %r' % self.id
 

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method =='POST':
        voucher_content = request.form['content']
        voucher_price = request.form['price']
        new_voucher = Voucher(content=voucher_content, price=voucher_price)

        try: 
            db.session.add(new_voucher)
            db.session.commit()
            return redirect('/')
        except:
            return 'There is an issue adding your voucher'
    else:   
        vouchers = Voucher.query.order_by(Voucher.date_created).all()
        return render_template('index.html', vouchers = vouchers)


@app.route('/delete/<int:id>')
def delete(id):
    voucher_to_delete = Voucher.query.get_or_404(id)
    try:
        db.session.delete(voucher_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting your voucher'


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):

    voucher = Voucher.query.get_or_404(id)
    
    if request.method == 'POST':
        voucher.content = request.form['content']
        voucher.price = request.form['price']
        try: 
            db.session.commit()
            return redirect('/')
        except:
            'There was a problem updating your voucher'
    else:
        return render_template('update.html')


if __name__ == "__name__":
    app.run(debug=True)  