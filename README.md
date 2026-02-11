# 🧠 P300 Oddball Test — All-in-One EEG Simulation Pipeline

이 저장소는 **Oddball 시각 자극 생성 → Oddball 기반 가짜 EEG 생성 → P300 ERP 추출 및 시각화**를  
하나의 Python 스크립트(`plot_p300_timeline.py`)로 자동 수행하는 실험/연구용 파이프라인입니다.

---

## 🚀 실행 방법

```bash
python plot_p300_timeline.py

실행 즉시 다음 3단계가 자동 진행됩니다:

1️⃣ Oddball 시각 자극 생성

길이: 10초

FPS: 1Hz

Oddball 확률: 60%

출력 파일:

results/oddball.gif

results/oddball_input.csv

2️⃣ Oddball 기반 24채널 Fake EEG 생성

샘플링 속도: 250 Hz

길이: 10초

Oddball 발생 후 +300 ms 위치에 Gaussian 형태의 P300 peak 삽입

Midline 채널(Fz / Pz / Cz)에 더 강하게 삽입

출력:

results/epoch_p300.csv

3️⃣ P300 ERP 추출 및 시각화

Oddball 기준 −0.2s ~ +0.8s epoching

Trial별 waveform + 평균 ERP 출력

Typical P300 window(0.25–0.45s) 강조 표시

실행 시 그래프 자동 팝업

📁 자동 생성 파일 (results/ 폴더)

파일명	설명

oddball.gif	10초 길이 Oddball 시각 자극
oddball_input.csv	프레임·타임스탬프·oddball 여부 기록
epoch_p300.csv	Oddball 기반으로 생성된 24채널 Fake EEG 신호

🧠 신호 처리 요약

EEG Sampling: 250 Hz

P300 Latency: 300 ms

Epoch Window: −0.2s ~ +0.8s

Midline(Fz / Pz / Cz) 채널에서 더 강한 P300 생성

🧩 채널 매핑 (총 24채널)
idx	name	idx	name	idx	name
ch0	Fp1	ch8	  O1	ch16	AFz
ch1	Fp2	ch9	  O2	ch17	Cz
ch2	F3	ch10	F7	ch18	T7
ch3	Fz	ch11	F8	ch19	Fpz
ch4	Pz	ch12	C3	ch20	T8
ch5	C4	ch13	T7	ch21	Oz
ch6	FC5	ch14	P7	ch22	AF3
ch7	FC6	ch15	P8	ch23	AF4

📦 의존성
pip install numpy pandas matplotlib pillow

📜 스크립트 설명
plot_p300_timeline.py

한 파일에서 다음을 모두 수행합니다:

Oddball GIF + 타임라인 CSV 생성

Oddball 기반 Fake EEG 생성

P300 ERP 분석 + 시각화
