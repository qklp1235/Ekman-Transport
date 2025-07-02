#!/usr/bin/env python3
"""
에크만 수송 계산 테스트 스크립트
"""

import numpy as np
from ekman_calculations import EkmanTransportCalculator

def test_ekman_calculations():
    """에크만 수송 계산 테스트"""
    print("🧪 에크만 수송 계산 테스트")
    print("=" * 50)
    
    # 계산기 인스턴스 생성
    calculator = EkmanTransportCalculator()
    
    # 테스트 파라미터
    test_cases = [
        {
            'name': '적도 근처 (저위도)',
            'wind_speed': 10,
            'wind_direction': 0,
            'latitude': 5,
            'depth': 100
        },
        {
            'name': '중위도',
            'wind_speed': 15,
            'wind_direction': 45,
            'latitude': 30,
            'depth': 200
        },
        {
            'name': '고위도',
            'wind_speed': 20,
            'wind_direction': 90,
            'latitude': 60,
            'depth': 500
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📊 테스트 케이스 {i}: {case['name']}")
        print("-" * 30)
        
        # 에크만 수송 계산
        results = calculator.calculate_ekman_transport(
            wind_speed=case['wind_speed'],
            wind_direction=case['wind_direction'],
            latitude=case['latitude'],
            depth=case['depth']
        )
        
        # 결과 출력
        print(f"바람 속도: {results['wind_speed']} m/s")
        print(f"바람 방향: {results['wind_direction']}°")
        print(f"위도: {results['latitude']}°")
        print(f"깊이: {results['depth']} m")
        print(f"바람 응력: {results['wind_stress']*1000:.2f} mN/m²")
        print(f"코리올리 매개변수: {results['f']*1e5:.3f} × 10⁻⁵ s⁻¹")
        print(f"에크만 깊이: {results['ekman_depth']:.1f} m")
        print(f"에크만 수송 (X): {results['Mx']*1e6:.2f} m³/s × 10⁶")
        print(f"에크만 수송 (Y): {results['My']*1e6:.2f} m³/s × 10⁶")
        print(f"총 수송량: {np.sqrt(results['Mx']**2 + results['My']**2)*1e6:.2f} m³/s × 10⁶")
        
        # 물리적 검증
        print("\n🔍 물리적 검증:")
        
        # 1. 코리올리 매개변수 검증
        expected_f = 2 * 7.2921e-5 * np.sin(np.radians(results['latitude']))
        print(f"  코리올리 매개변수 검증: {'✅' if abs(results['f'] - expected_f) < 1e-10 else '❌'}")
        
        # 2. 바람 응력 검증
        expected_stress = 1.225 * 0.0013 * results['wind_speed']**2
        print(f"  바람 응력 검증: {'✅' if abs(results['wind_stress'] - expected_stress) < 1e-10 else '❌'}")
        
        # 3. 에크만 수송 방향 검증 (바람에 대해 90도)
        wind_angle = np.arctan2(results['tau_y'], results['tau_x'])
        transport_angle = np.arctan2(results['My'], results['Mx'])
        angle_diff = abs(wind_angle - transport_angle)
        print(f"  수송 방향 검증 (90도): {'✅' if abs(angle_diff - np.pi/2) < 0.1 else '❌'}")
    
    print("\n" + "=" * 50)
    print("✅ 모든 테스트 완료!")
    
    # 시각화 테스트
    print("\n🎨 시각화 테스트")
    print("-" * 30)
    
    # 2D 시각화 테스트
    test_results = calculator.calculate_ekman_transport(10, 0, 30, 100)
    try:
        fig_2d = calculator.create_2d_visualization(test_results)
        print("✅ 2D 시각화 생성 성공")
    except Exception as e:
        print(f"❌ 2D 시각화 생성 실패: {e}")
    
    # 3D 시각화 테스트
    try:
        fig_3d = calculator.create_3d_visualization(test_results)
        print("✅ 3D 시각화 생성 성공")
    except Exception as e:
        print(f"❌ 3D 시각화 생성 실패: {e}")

if __name__ == "__main__":
    test_ekman_calculations() 