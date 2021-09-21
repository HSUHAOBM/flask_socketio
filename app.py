from flask import *
from flask_socketio import SocketIO,emit,join_room,leave_room
from werkzeug import debug

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEYsecret!"
socketio = SocketIO(app)




#首頁
@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST" and request.form["user"] and request.form["room"]:
        session["user"]=request.form["user"]
        session["room"]=request.form["room"]
        return redirect(url_for("chat"))
    return render_template("home.html")

#聊天室
@app.route("/chat")
def chat():
    room = session["room"]
    return render_template("index.html",room = room)

@socketio.on("my event",namespace="/chat")
def index(data):
    emit("status",data['data'])
    join_room(session.get("room"))

@socketio.on("text",namespace="/chat")
def get_msg(data):
    room = session["room"]
    emit("message",session["user"]+" : "+data,room = room)



@socketio.on("left",namespace="/chat")
def leave(data):
    room = session["room"]
    leave_room(session["room"])
    print(data)
    emit("message",session["user"]+" leave the room \n",room = room)

@socketio.on("broadcast",namespace="/chat")
def broadcast(data):
    emit("message",session["user"]+" from "+session["room"]+"  "+data+" \n",broadcast=True)

if __name__ == "__main__":
    # socketio.run(app, port=6500)
    socketio.run(app, host="0.0.0.0", port=5000)
