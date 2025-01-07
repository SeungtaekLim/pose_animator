from ultralytics import YOLO
import cv2

# YOLO 모델을 로드 (여기서는 자세 추정 모델을 로드한다고 가정)
model = YOLO("yolo11m-pose.pt")  # pose 추정 모델을 로드

# 비디오 파일 경로 지정
video_path = "cam.mp4"

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 비디오의 프레임 크기 및 FPS 정보 가져오기
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 동영상 출력 객체 생성 (파일로 저장)
output_video_path = "output_video.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 형식으로 저장
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# 키포인트 좌표를 저장할 텍스트 파일 열기
keypoints_file = open("keypoints_detail.txt", "w")
keypoints2_file = open("keypoints.txt", "w")

# 비디오에서 프레임 하나씩 읽어오기
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 프레임을 모델에 넣어 예측 수행
    results = model(frame)  # 프레임을 모델에 넣어 예측
    
    # 예측된 프레임을 출력
    annotated_frame = results[0].plot()  # 예측 결과가 그려진 프레임 얻기

    # keypoints 추출
    keypoints = results[0].keypoints  # keypoints를 얻기
    
    # keypoints.xy: (x, y) 좌표, keypoints.conf: 각 keypoint의 confidence
    xy = keypoints.xy  # 픽셀 좌표
    conf = keypoints.conf  # 신뢰도

    # 각 키포인트의 좌표와 신뢰도를 텍스트 파일에 저장
    keypoints_text = "Frame {} Keypoints:\n".format(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
    
    for i in range(len(xy[0])):  # 각 사람마다 반복
        x, y = xy[0][i]  # (x, y) 좌표
        c = conf[0][i]  # 각 키포인트의 신뢰도
        
        # 텍스트 파일에 좌표와 신뢰도 저장
        keypoints_text += "Keypoint {}: ({:.2f}, {:.2f}), Confidence: {:.2f}\n".format(i, x, y, c)
    
    # 텍스트 파일에 키포인트 좌표 저장
    keypoints_file.write(keypoints_text + "\n")
    
    # Keypoints2.txt에 프레임 번호와 키포인트 좌표만 저장
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))  # 현재 프레임 번호
    keypoints2_text = f"{frame_number} "  # 프레임 번호로 시작
    
    # 17개의 키포인트 좌표를 한 줄로 저장
    for i in range(len(xy[0])):
        x, y = xy[0][i]  # (x, y) 좌표
        keypoints2_text += f"{x:.2f} {y:.2f} "  # x, y 좌표를 추가
    
    keypoints2_file.write(keypoints2_text.strip() + "\n")  # 한 줄 끝에 공백을 없애고 저장

    # 프레임을 동영상 파일로 저장
    out.write(annotated_frame)

    # 결과 화면에 표시 (선택 사항)
    cv2.imshow('Annotated Frame', annotated_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
out.release()
cv2.destroyAllWindows()

# 텍스트 파일 닫기
keypoints_file.close()
keypoints2_file.close()
