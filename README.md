# eeg_p300_test

📘 P300 Oddball Test — All-in-One Pipeline

이 프로젝트는 Oddball 자극 생성 → Oddball 기반 가짜 EEG 생성 → P300 ERP 추출 & 시각화까지
모든 단계를 하나의 Python 스크립트에서 자동으로 실행하는 연구 테스트 파이프라인입니다.

🚀 실행 방법
python plot_p300_timeline.py


실행 즉시 다음이 자동 수행됩니다:

oddball 스티뮬러스 생성

10초 / FPS=1Hz / 60% Oddball(빨간 화면)

results/oddball.gif

results/oddball_input.csv

가짜 EEG 생성 (Oddball 기반)

24채널 / 250Hz / 10초

Oddball 이후 +300ms 위치에 Gaussian P300 peak 자동 삽입

results/epoch_p300.csv

P300 ERP 시각화

oddball 기준 -200ms ~ +800ms epoching

ERP 평균 그래프 팝업

📁 자동 생성 파일 (results/ 폴더)
파일명	설명
oddball.gif	10초짜리 Oddball 시각 자극
oddball_input.csv	프레임·타임스탬프·oddball 여부 기록
epoch_p300.csv	Oddball 기반으로 생성된 24채널 Fake EEG
(그래프)	실행 시 P300 ERP plot 표시
🧠 신호 처리 요약

EEG 샘플링: 250 Hz

P300 latency: 300 ms

Epoch window: −0.2s ~ +0.8s

Midline(Fz/Pz/Cz) 채널에 더 강한 P300 삽입

🧩 채널 매핑 (24ch)
idx	name	idx	name	idx	name
ch0	Fp1	ch8	O1	ch16	AFz
ch1	Fp2	ch9	O2	ch17	Cz
ch2	F3	ch10	F7	ch18	T7
ch3	Fz	ch11	F8	ch19	Fpz
ch4	Pz	ch12	C3	ch20	T8
ch5	C4	ch13	T7	ch21	Oz
ch6	FC5	ch14	P7	ch22	AF3
ch7	FC6	ch15	P8	ch23	AF4
