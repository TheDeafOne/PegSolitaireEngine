from flask import Flask, render_template

class WebappVisualizer:
    app = Flask(__name__)

    @app.route('/')
    def _run_app():
        return render_template('main.html',chr=chr)

    # @app.route('/submit/<initial_state>/<goal_state>')
    # def submit_board(initial_state, goal_state):
    #     pass

    # @app.route('run')
    def visualize(self):
        self.app.run(debug=True)