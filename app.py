from flask import Flask, render_template, jsonify, request
import numpy as np
import plotly.graph_objects as go
import plotly.utils
import json
from ekman_calculations import EkmanTransportCalculator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_ekman', methods=['POST'])
def calculate_ekman():
    data = request.get_json()
    
    # 파라미터 추출
    wind_speed = float(data.get('wind_speed', 10))  # m/s
    wind_direction = float(data.get('wind_direction', 0))  # degrees
    latitude = float(data.get('latitude', 30))  # degrees
    depth = float(data.get('depth', 100))  # meters
    visualization_type = data.get('visualization_type', '3d')
    
    # 에크만 수송 계산
    calculator = EkmanTransportCalculator()
    results = calculator.calculate_ekman_transport(
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        latitude=latitude,
        depth=depth
    )
    
    # 시각화 생성
    if visualization_type == '3d':
        fig = calculator.create_3d_visualization(results)
    else:
        fig = calculator.create_2d_visualization(results)
    
    # Plotly 그래프를 JSON으로 변환
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'graph': graph_json,
        'results': results
    })

@app.route('/get_parameters')
def get_parameters():
    """기본 파라미터 값들을 반환"""
    return jsonify({
        'wind_speed_range': [0, 30],
        'wind_direction_range': [0, 360],
        'latitude_range': [-90, 90],
        'depth_range': [10, 1000],
        'default_values': {
            'wind_speed': 10,
            'wind_direction': 0,
            'latitude': 30,
            'depth': 100
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 