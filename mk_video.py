import cv2

# 웹캠 초기화 (0번 카메라 사용)
cap = cv2.VideoCapture(0)

# 비디오의 프레임 크기 설정
frame_width = int(cap.get(3))  # 프레임 너비
frame_height = int(cap.get(4))  # 프레임 높이

# 비디오 출력 설정 (저장할 파일 이름, 코덱, 프레임 속도, 프레임 크기)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4V 코덱 사용
out = None  # 비디오 출력을 초기화하지 않음

is_recording = False  # 촬영 여부를 나타내는 변수

while True:
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 's' 키를 누르면 비디오 녹화 시작
    if cv2.waitKey(1) & 0xFF == ord('s') and not is_recording:
        is_recording = True
        out = cv2.VideoWriter('cam.mp4', fourcc, 20.0, (frame_width, frame_height))
        print("녹화 시작!")

    # 녹화 중일 때만 프레임을 저장
    if is_recording:
        out.write(frame)

    # 프레임을 화면에 출력
    cv2.imshow('Webcam Video', frame)

    # 'q' 키를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠과 비디오 파일을 닫기
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()
