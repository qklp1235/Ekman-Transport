// 메인 JavaScript 파일
document.addEventListener('DOMContentLoaded', function() {
    // DOM 요소들
    const form = document.getElementById('ekmanForm');
    const windSpeedSlider = document.getElementById('windSpeed');
    const windDirectionSlider = document.getElementById('windDirection');
    const latitudeSlider = document.getElementById('latitude');
    const depthSlider = document.getElementById('depth');
    const windSpeedValue = document.getElementById('windSpeedValue');
    const windDirectionValue = document.getElementById('windDirectionValue');
    const latitudeValue = document.getElementById('latitudeValue');
    const depthValue = document.getElementById('depthValue');
    const visualizationContainer = document.getElementById('visualizationContainer');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsPanel = document.getElementById('resultsPanel');
    const visualizationTitle = document.getElementById('visualizationTitle');

    // 슬라이더 값 업데이트 함수들
    function updateWindSpeed() {
        windSpeedValue.textContent = windSpeedSlider.value;
    }

    function updateWindDirection() {
        windDirectionValue.textContent = windDirectionSlider.value + '°';
    }

    function updateLatitude() {
        latitudeValue.textContent = latitudeSlider.value + '°';
    }

    function updateDepth() {
        depthValue.textContent = depthSlider.value + 'm';
    }

    // 이벤트 리스너 등록
    windSpeedSlider.addEventListener('input', updateWindSpeed);
    windDirectionSlider.addEventListener('input', updateWindDirection);
    latitudeSlider.addEventListener('input', updateLatitude);
    depthSlider.addEventListener('input', updateDepth);

    // 폼 제출 이벤트
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        calculateEkmanTransport();
    });

    // 에크만 수송 계산 함수
    async function calculateEkmanTransport() {
        // 로딩 상태 표시
        showLoading();

        // 폼 데이터 수집
        const formData = {
            wind_speed: parseFloat(windSpeedSlider.value),
            wind_direction: parseFloat(windDirectionSlider.value),
            latitude: parseFloat(latitudeSlider.value),
            depth: parseFloat(depthSlider.value),
            visualization_type: document.querySelector('input[name="visualizationType"]:checked').value
        };

        try {
            // 서버에 요청 보내기
            const response = await fetch('/calculate_ekman', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // 시각화 표시
            displayVisualization(data.graph, formData.visualization_type);
            
            // 결과 패널 업데이트
            updateResultsPanel(data.results);
            
        } catch (error) {
            console.error('Error:', error);
            showError('계산 중 오류가 발생했습니다. 다시 시도해주세요.');
        } finally {
            hideLoading();
        }
    }

    // 로딩 상태 표시
    function showLoading() {
        loadingSpinner.classList.remove('d-none');
        visualizationContainer.innerHTML = '';
    }

    // 로딩 상태 숨기기
    function hideLoading() {
        loadingSpinner.classList.add('d-none');
    }

    // 에러 표시
    function showError(message) {
        visualizationContainer.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
            </div>
        `;
    }

    // 시각화 표시
    function displayVisualization(graphData, type) {
        const graph = JSON.parse(graphData);
        
        // 시각화 타입에 따른 제목 업데이트
        if (type === '3d') {
            visualizationTitle.textContent = '3D 에크만 수송 시각화';
        } else {
            visualizationTitle.textContent = '2D 에크만 수송 분석';
        }

        // Plotly 그래프 생성
        Plotly.newPlot(visualizationContainer, graph.data, graph.layout, {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        });

        // 애니메이션 효과 추가
        visualizationContainer.classList.add('fade-in');
    }

    // 결과 패널 업데이트
    function updateResultsPanel(results) {
        const resultsHtml = `
            <div class="result-item">
                <span class="result-label">바람 응력:</span>
                <span class="result-value">${(results.wind_stress * 1000).toFixed(2)} mN/m²</span>
            </div>
            <div class="result-item">
                <span class="result-label">에크만 수송 (X):</span>
                <span class="result-value">${(results.Mx * 1e6).toFixed(2)} m³/s × 10⁶</span>
            </div>
            <div class="result-item">
                <span class="result-label">에크만 수송 (Y):</span>
                <span class="result-value">${(results.My * 1e6).toFixed(2)} m³/s × 10⁶</span>
            </div>
            <div class="result-item">
                <span class="result-label">에크만 깊이:</span>
                <span class="result-value">${results.ekman_depth.toFixed(1)} m</span>
            </div>
            <div class="result-item">
                <span class="result-label">코리올리 매개변수:</span>
                <span class="result-value">${(results.f * 1e5).toFixed(3)} × 10⁻⁵ s⁻¹</span>
            </div>
            <div class="result-item">
                <span class="result-label">총 수송량:</span>
                <span class="result-value">${(Math.sqrt(results.Mx**2 + results.My**2) * 1e6).toFixed(2)} m³/s × 10⁶</span>
            </div>
        `;
        
        resultsPanel.innerHTML = resultsHtml;
        resultsPanel.classList.add('fade-in');
    }

    // 초기 값 설정
    updateWindSpeed();
    updateWindDirection();
    updateLatitude();
    updateDepth();

    // 키보드 단축키
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter로 계산 실행
        if (e.ctrlKey && e.key === 'Enter') {
            calculateEkmanTransport();
        }
        
        // ESC로 로딩 취소
        if (e.key === 'Escape') {
            hideLoading();
        }
    });

    // 실시간 미리보기 (선택적)
    let previewTimeout;
    function setupRealTimePreview() {
        const sliders = [windSpeedSlider, windDirectionSlider, latitudeSlider, depthSlider];
        
        sliders.forEach(slider => {
            slider.addEventListener('input', function() {
                clearTimeout(previewTimeout);
                previewTimeout = setTimeout(() => {
                    // 빠른 미리보기 계산 (선택적 기능)
                    // calculateEkmanTransport();
                }, 1000);
            });
        });
    }

    // 실시간 미리보기 설정 (주석 처리 - 성능상 이유)
    // setupRealTimePreview();

    // 도구팁 초기화
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 반응형 처리
    function handleResize() {
        if (window.innerWidth < 768) {
            // 모바일에서 시각화 크기 조정
            const plotlyDiv = document.querySelector('.plotly-graph-div');
            if (plotlyDiv) {
                Plotly.relayout(plotlyDiv, {
                    width: window.innerWidth - 40,
                    height: 400
                });
            }
        }
    }

    window.addEventListener('resize', handleResize);

    // 페이지 로드 시 초기 계산 (선택적)
    // setTimeout(() => {
    //     calculateEkmanTransport();
    // }, 1000);
}); 