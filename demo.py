#!/usr/bin/env python3
"""
에크만 수송 데모 스크립트
간단한 계산과 결과 출력
"""

import math

def calculate_coriolis_parameter(latitude_degrees):
    """코리올리 매개변수 계산"""
    omega = 7.2921e-5  # 지구 자전 각속도 (rad/s)
    latitude_rad = math.radians(latitude_degrees)
    return 2 * omega * math.sin(latitude_rad)

def calculate_wind_stress(wind_speed):
    """바람 응력 계산"""
    rho_air = 1.225  # 공기 밀도 (kg/m³)
    Cd = 0.0013      # 항력 계수
    return rho_air * Cd * wind_speed**2

def calculate_ekman_transport(wind_speed, wind_direction, latitude):
    """에크만 수송 계산"""
    # 코리올리 매개변수
    f = calculate_coriolis_parameter(latitude)
    
    # 바람 응력
    wind_stress = calculate_wind_stress(wind_speed)
    
    # 바람 방향을 라디안으로 변환
    wind_direction_rad = math.radians(wind_direction)
    
    # 바람 응력의 x, y 성분
    tau_x = wind_stress * math.cos(wind_direction_rad)
    tau_y = wind_stress * math.sin(wind_direction_rad)
    
    # 에크만 수송 계산
    rho_water = 1025  # 해수 밀도 (kg/m³)
    Mx = -tau_y / (rho_water * f)
    My = tau_x / (rho_water * f)
    
    return {
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'latitude': latitude,
        'wind_stress': wind_stress,
        'tau_x': tau_x,
        'tau_y': tau_y,
        'Mx': Mx,
        'My': My,
        'f': f
    }

def main():
    print("🌊 에크만 수송 계산 데모")
    print("=" * 50)
    
    # 테스트 케이스들
    test_cases = [
        (10, 0, 30, "중위도, 동쪽 바람"),
        (15, 45, 45, "고위도, 북동쪽 바람"),
        (5, 90, 10, "저위도, 북쪽 바람")
    ]
    
    for wind_speed, wind_direction, latitude, description in test_cases:
        print(f"\n📊 {description}")
        print("-" * 30)
        
        results = calculate_ekman_transport(wind_speed, wind_direction, latitude)
        
        print(f"바람 속도: {results['wind_speed']} m/s")
        print(f"바람 방향: {results['wind_direction']}°")
        print(f"위도: {results['latitude']}°")
        print(f"바람 응력: {results['wind_stress']*1000:.2f} mN/m²")
        print(f"코리올리 매개변수: {results['f']*1e5:.3f} × 10⁻⁵ s⁻¹")
        print(f"에크만 수송 (X): {results['Mx']*1e6:.2f} m³/s × 10⁶")
        print(f"에크만 수송 (Y): {results['My']*1e6:.2f} m³/s × 10⁶")
        
        # 총 수송량 계산
        total_transport = math.sqrt(results['Mx']**2 + results['My']**2)
        print(f"총 수송량: {total_transport*1e6:.2f} m³/s × 10⁶")
        
        # 수송 방향 계산
        transport_direction = math.degrees(math.atan2(results['My'], results['Mx']))
        print(f"수송 방향: {transport_direction:.1f}°")
        
        # 바람과 수송의 각도 차이 (이론적으로 90도)
        wind_angle = math.atan2(results['tau_y'], results['tau_x'])
        transport_angle = math.atan2(results['My'], results['Mx'])
        angle_diff = abs(wind_angle - transport_angle)
        print(f"바람-수송 각도 차이: {math.degrees(angle_diff):.1f}° (이론값: 90°)")
    
    print("\n" + "=" * 50)
    print("✅ 데모 완료!")
    print("\n💡 주요 특징:")
    print("- 바람 방향에 대해 수송은 90도 각도로 발생")
    print("- 위도가 높을수록 코리올리 힘이 강해짐")
    print("- 바람 속도가 강할수록 수송량이 증가")
    print("- 에크만 수송은 해양 순환의 중요한 메커니즘")

if __name__ == "__main__":
    main() 