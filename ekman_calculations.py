import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from translations import translations

class EkmanTransportCalculator:
    def __init__(self):
        # 물리 상수
        self.rho_water = 1025  # kg/m³ (해수 밀도)
        self.rho_air = 1.225   # kg/m³ (공기 밀도)
        self.Cd = 0.0013       # 항력 계수
        self.f = None          # 코리올리 매개변수 (위도에 따라 계산)
        
    def _set_matplotlib_font(self, lang):
        """언어에 따라 Matplotlib 폰트를 설정합니다."""
        # 언어별 폰트 설정
        font_family_map = {
            'en': 'Apple SD Gothic Neo',
            'ko': 'Apple SD Gothic Neo',
            'zh': 'Apple SD Gothic Neo',
            'ja': 'Apple SD Gothic Neo',
            'ru': 'Apple SD Gothic Neo',
            'es': 'Apple SD Gothic Neo'
        }
        font_name = font_family_map.get(lang, 'Apple SD Gothic Neo')
        try:
            plt.rcParams['font.family'] = font_name
            plt.rcParams['axes.unicode_minus'] = False
        except Exception as e:
            print(f"폰트 '{font_name}' 설정 실패: {e}")
            # 대체 폰트 설정
            plt.rcParams['font.family'] = 'Apple SD Gothic Neo'
            plt.rcParams['axes.unicode_minus'] = False
        
    def calculate_coriolis_parameter(self, latitude):
        """코리올리 매개변수 계산"""
        omega = 7.2921e-5  # 지구 자전 각속도 (rad/s)
        return 2 * omega * np.sin(np.radians(latitude))
    
    def calculate_ekman_transport(self, wind_speed, wind_direction, latitude, depth):
        """에크만 수송 계산"""
        if latitude == 0:
            latitude = 1e-6 # 위도가 0일 때 f가 0이 되어 나누기 오류가 발생하는 것을 방지

        # 코리올리 매개변수 계산
        f = self.calculate_coriolis_parameter(latitude)
        
        # 바람 응력 계산
        wind_stress = self.rho_air * self.Cd * wind_speed**2
        
        # 바람 방향을 라디안으로 변환
        wind_direction_rad = np.radians(wind_direction)
        
        # 바람 응력의 x, y 성분
        tau_x = wind_stress * np.cos(wind_direction_rad)
        tau_y = wind_stress * np.sin(wind_direction_rad)
        
        # 에크만 수송 계산 (Ekman, 1905)
        # Mx = -τy / (ρf), My = τx / (ρf)
        Mx = -tau_y / (self.rho_water * f)
        My = tau_x / (self.rho_water * f)
        
        # 에크만 깊이 및 표층 해류 계산을 위한 상수
        K = 0.01  # m²/s (일반적인 수직 난류 점성 계수)
        ekman_depth = np.pi * np.sqrt(2 * K / abs(f))
        
        # 수직 속도 프로파일 생성 (에크만 나선)
        z_levels = np.linspace(0, depth, 50)
        ekman_spiral = self.calculate_ekman_spiral(z_levels, tau_x, tau_y, f, K)

        # 표층 해류 속도 (z=0)
        u_surface = ekman_spiral['u'][0]
        v_surface = ekman_spiral['v'][0]
        
        # 에너지 전달률 계산 (단위 면적당 일률, W/m^2)
        energy_transfer_rate = tau_x * u_surface + tau_y * v_surface
        
        results = {
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'latitude': latitude,
            'depth': depth,
            'wind_stress': wind_stress,
            'tau_x': tau_x,
            'tau_y': tau_y,
            'Mx': Mx,
            'My': My,
            'ekman_depth': ekman_depth,
            'z_levels': z_levels,
            'ekman_spiral': ekman_spiral,
            'f': f,
            'energy_transfer_rate': energy_transfer_rate
        }
        
        return results
    
    def calculate_ekman_spiral(self, z_levels, tau_x, tau_y, f, K):
        """에크만 나선 계산"""
        # a = sqrt(|f| / 2K)
        a = np.sqrt(abs(f) / (2 * K))
        
        # 공통 계수
        factor = np.exp(-a * z_levels) / (self.rho_water * np.sqrt(2 * K * abs(f)))
        
        # 속도 성분
        cos_az, sin_az = np.cos(a * z_levels), np.sin(a * z_levels)
        sgn_f = np.sign(f)
        
        u = factor * (tau_x * cos_az - sgn_f * tau_y * sin_az)
        v = factor * (sgn_f * tau_x * sin_az + tau_y * cos_az)
        
        return {'u': u, 'v': v}
    
    def _create_matplotlib_3d(self, fig, results, lang='en'):
        """Matplotlib 3D 시각화 생성"""
        self._set_matplotlib_font(lang)
        t = translations.get(lang, translations['en'])

        ax = fig.add_subplot(111, projection='3d')
        
        z_levels, spiral = results['z_levels'], results['ekman_spiral']
        u, v = spiral['u'], spiral['v']
        speeds = np.sqrt(u**2 + v**2)
        max_speed = np.max(speeds) if np.max(speeds) > 0 else 1.0

        cmap = plt.get_cmap('viridis')
        norm = plt.Normalize(vmin=0, vmax=max_speed)
        
        for i in range(len(z_levels)):
            ax.quiver(0, 0, -z_levels[i], u[i], v[i], 0, 
                      color=cmap(norm(speeds[i])), length=0.1, normalize=True)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, shrink=0.6, aspect=15, label=t['colorbar_3d'])

        wind_speed = results['wind_speed']
        wind_direction_rad = np.radians(results['wind_direction'])
        wind_plot_len = max_speed 
        wind_x = wind_plot_len * np.cos(wind_direction_rad)
        wind_y = wind_plot_len * np.sin(wind_direction_rad)
        
        ax.quiver(0, 0, 5, wind_x, wind_y, 0, color='orange', label=t['wind_label_3d'].format(wind_speed=wind_speed), lw=2,
                  arrow_length_ratio=0.2, length=0.1, normalize=True)

        ax.set_xlabel(t['xlabel_3d'])
        ax.set_ylabel(t['ylabel_3d'])
        ax.set_zlabel(t['zlabel_3d'])
        ax.set_title(t['plot_title_3d'])
        ax.legend()
        ax.view_init(elev=30, azim=-60)

    def _create_matplotlib_2d(self, fig, results, lang='en'):
        """Matplotlib 2D 시각화 생성"""
        self._set_matplotlib_font(lang)
        t = translations.get(lang, translations['en'])

        gs = fig.add_gridspec(2, 2)

        ax1 = fig.add_subplot(gs[0, 0])
        wind_speed = results['wind_speed']
        wind_dir_rad = np.radians(results['wind_direction'])
        wind_x, wind_y = wind_speed * np.cos(wind_dir_rad), wind_speed * np.sin(wind_dir_rad)
        
        transport_mag = np.sqrt(results['Mx']**2 + results['My']**2)
        scale_factor = wind_speed / transport_mag if transport_mag > 0 else 1.0

        ax1.arrow(0, 0, wind_x, wind_y, head_width=0.5, head_length=0.7, fc='orange', ec='orange', label=t['wind_label_2d'].format(wind_speed=wind_speed))
        ax1.arrow(0, 0, results['Mx'] * scale_factor, results['My'] * scale_factor, head_width=0.5, head_length=0.7, fc='blue', ec='blue', label=t['transport_label_2d'].format(transport_mag=transport_mag))
        ax1.set_title(t['title_2d_transport'])
        ax1.set_xlabel(t['xlabel_2d_transport'])
        ax1.set_ylabel(t['ylabel_2d_transport'])
        ax1.grid(True)
        ax1.legend()
        ax1.set_aspect('equal', adjustable='box')

        ax2 = fig.add_subplot(gs[0, 1])
        spiral = results['ekman_spiral']
        z_levels = results['z_levels']
        points = np.array([spiral['u'], spiral['v']]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        norm = plt.Normalize(z_levels.min(), z_levels.max())
        lc = LineCollection(segments, cmap='plasma', norm=norm)
        lc.set_array(z_levels)
        lc.set_linewidth(3)
        line = ax2.add_collection(lc)
        fig.colorbar(line, ax=ax2, label=t['colorbar_2d_spiral'])

        ax2.set_title(t['title_2d_spiral'])
        ax2.set_xlabel(t['xlabel_2d_spiral'])
        ax2.set_ylabel(t['ylabel_2d_spiral'])
        ax2.grid(True)
        ax2.autoscale_view()
        ax2.set_aspect('equal', adjustable='box')

        ax3 = fig.add_subplot(gs[1, 0])
        ax3.plot(spiral['u'], -results['z_levels'], 'b-', label=t['u_velocity_label'])
        ax3.plot(spiral['v'], -results['z_levels'], 'r-', label=t['v_velocity_label'])
        ax3.set_title(t['title_2d_profile'])
        ax3.set_xlabel(t['xlabel_2d_profile'])
        ax3.set_ylabel(t['ylabel_2d_profile'])
        ax3.grid(True)
        ax3.legend()

        ax4 = fig.add_subplot(gs[1, 1])
        components = ['Mx', 'My']
        values = [results['Mx'], results['My']]
        ax4.bar(components, values, color=['blue', 'red'])
        ax4.set_title(t['title_2d_components'])
        ax4.set_ylabel(t['ylabel_2d_components'])
        ax4.grid(axis='y') 
        fig.suptitle(t['plot_title_2d'], fontsize=16)
    
    def create_3d_visualization(self, results, lang='ko'):
        """Plotly 3D 시각화 생성"""
        import plotly.graph_objects as go
        
        z_levels = results['z_levels']
        spiral = results['ekman_spiral']
        u, v = spiral['u'], spiral['v']
        
        # 속도 크기 계산
        speeds = np.sqrt(u**2 + v**2)
        max_speed = np.max(speeds) if np.max(speeds) > 0 else 1.0
        
        # 3D 벡터 필드 생성
        fig = go.Figure()
        
        # 에크만 나선 벡터들
        for i in range(0, len(z_levels), 3):  # 일부만 표시
            fig.add_trace(go.Scatter3d(
                x=[0, u[i]*10],
                y=[0, v[i]*10],
                z=[-z_levels[i], -z_levels[i]],
                mode='lines+markers',
                line=dict(color=f'rgb({int(255*speeds[i]/max_speed)}, {int(128*(1-speeds[i]/max_speed))}, 255)', width=3),
                marker=dict(size=3),
                showlegend=False,
                name=f'깊이 {z_levels[i]:.1f}m'
            ))
        
        # 바람 벡터 추가
        wind_speed = results['wind_speed']
        wind_direction_rad = np.radians(results['wind_direction'])
        wind_x = wind_speed * np.cos(wind_direction_rad)
        wind_y = wind_speed * np.sin(wind_direction_rad)
        
        fig.add_trace(go.Scatter3d(
            x=[0, wind_x],
            y=[0, wind_y],
            z=[5, 5],
            mode='lines+markers',
            line=dict(color='orange', width=8),
            marker=dict(size=8, color='orange'),
            name=f'바람 {wind_speed:.1f} m/s'
        ))
        
        # 레이아웃 설정
        fig.update_layout(
            title='에크만 수송 3D 시각화',
            scene=dict(
                xaxis_title='동-서 방향 (m/s)',
                yaxis_title='남-북 방향 (m/s)',
                zaxis_title='깊이 (m)',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            width=800,
            height=600,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        return fig
    
    def create_2d_visualization(self, results, lang='ko'):
        """Plotly 2D 시각화 생성"""
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # 2x2 서브플롯 생성
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('바람 vs 수송', '에크만 나선', '깊이별 속도', '수송 성분'),
            specs=[[{"type": "xy"}, {"type": "xy"}],
                   [{"type": "xy"}, {"type": "xy"}]]
        )
        
        # 1. 바람 vs 수송 벡터
        wind_speed = results['wind_speed']
        wind_dir_rad = np.radians(results['wind_direction'])
        wind_x = wind_speed * np.cos(wind_dir_rad)
        wind_y = wind_speed * np.sin(wind_dir_rad)
        
        fig.add_trace(go.Scatter(
            x=[0, wind_x], y=[0, wind_y],
            mode='lines+markers',
            line=dict(color='orange', width=4),
            marker=dict(size=8),
            name='바람',
        ), row=1, col=1)
        
        transport_scale = 1e6
        fig.add_trace(go.Scatter(
            x=[0, results['Mx']*transport_scale], 
            y=[0, results['My']*transport_scale],
            mode='lines+markers',
            line=dict(color='blue', width=4),
            marker=dict(size=8),
            name='수송',
        ), row=1, col=1)
        
        # 2. 에크만 나선
        spiral = results['ekman_spiral']
        fig.add_trace(go.Scatter(
            x=spiral['u'], y=spiral['v'],
            mode='lines+markers',
            line=dict(color='red', width=2),
            marker=dict(size=3),
            name='에크만 나선',
        ), row=1, col=2)
        
        # 3. 깊이별 속도 프로파일
        z_levels = results['z_levels']
        fig.add_trace(go.Scatter(
            x=spiral['u'], y=-z_levels,
            mode='lines',
            line=dict(color='blue', width=2),
            name='U 속도',
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=spiral['v'], y=-z_levels,
            mode='lines',
            line=dict(color='red', width=2),
            name='V 속도',
        ), row=2, col=1)
        
        # 4. 수송 성분 바 차트
        fig.add_trace(go.Bar(
            x=['Mx', 'My'],
            y=[results['Mx'], results['My']],
            marker_color=['blue', 'red'],
            name='수송 성분',
        ), row=2, col=2)
        
        fig.update_layout(
            title='에크만 수송 2D 분석',
            height=800,
            showlegend=True
        )
        
        return fig 