import pygame
import time
import cv2
import math

# Pygame 초기화
pygame.init()

# 동영상 파일 경로
video_file = 'cam.mp4'

# 동영상 읽기
cap = cv2.VideoCapture(video_file)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 화면 크기 설정 (동영상의 해상도에 맞추기)
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Keypoint Animation")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # 선 색상

# 키포인트 크기 (원 크기)
KEYPOINT_RADIUS = 5

# 데이터 파일 경로
input_file = 'Keypoints.txt'

# 키포인트 이름 (순서대로, 영어로 변경)
KEYPOINT_NAMES = [
    "Nose", "Left Eye", "Right Eye", "Left Ear", "Right Ear", 
    "Left Shoulder", "Right Shoulder", "Left Elbow", "Right Elbow", 
    "Left Wrist", "Right Wrist", "Left Hip", "Right Hip", 
    "Left Knee", "Right Knee", "Left Ankle", "Right Ankle"
]

# 데이터를 읽어오는 함수
def read_keypoints(file_path):
    keypoints_data = []
    with open(file_path, 'r') as f:
        for line in f:
            data = line.split()
            frame_number = int(data[0])
            keypoints = list(map(float, data[1:]))
            keypoints_data.append((frame_number, keypoints))
    return keypoints_data

# Keypoints 데이터를 읽어옵니다.
keypoints_data = read_keypoints(input_file)

# 선분의 중심과 위쪽 방향으로 속이 빈 원을 그리는 함수
def draw_perpendicular_circle(screen, p1, p2, color):
    # 두 점 p1, p2의 중심 계산
    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2

    # 선분의 길이 계산
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.sqrt(dx**2 + dy**2)

    # 선분의 길이의 절반을 반지름으로 설정
    radius = length / 2

    # 위쪽 방향으로 수직 벡터 설정
    perp_dx = 0
    perp_dy = -1  # 위쪽 방향

    # 중심에서 수직 방향으로 이동 (반지름 길이만큼)
    circle_center = (mid_x + perp_dx * radius, mid_y + perp_dy * radius)

    # 원을 테두리만 그리기 위해 width를 2로 설정
    pygame.draw.circle(screen, color, (int(circle_center[0]), int(circle_center[1])), int(radius), width=2)

# 동영상 저장을 위한 설정 (OpenCV 사용)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4v 코덱 사용
output_video = cv2.VideoWriter('animation.mp4', fourcc, 25, (WIDTH, HEIGHT))  # 초당 25프레임으로 저장

def animate_keypoints():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)  # 텍스트를 그리기 위한 폰트 설정

    # 애니메이션 루프
    running = True
    current_frame = 0

    while running:
        # 이벤트 처리 (창을 닫을 때 종료)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 화면 배경을 흰색으로 지우기
        screen.fill(WHITE)

        # 현재 프레임에 해당하는 키포인트 좌표 가져오기
        if current_frame < len(keypoints_data):
            _, keypoints = keypoints_data[current_frame]

            keypoint_positions = []

            # 그리지 않도록 제외할 키포인트 인덱스를 지정
            exclude_keypoints = ["Nose", "Left Eye", "Right Eye", "Left Ear", "Right Ear"]

            for i in range(0, len(keypoints), 2):
                x = keypoints[i]
                y = keypoints[i + 1]

                # 키포인트 이름을 확인하여 제외할 리스트에 포함되지 않은 경우만 그리기
                if KEYPOINT_NAMES[i // 2] not in exclude_keypoints:
                    # x, y 값이 0이 아니면 키포인트를 그리기
                    if x != 0 and y != 0:
                        pygame.draw.circle(screen, RED, (int(x), int(y)), KEYPOINT_RADIUS)

                        # 키포인트 이름 텍스트 그리기 (원 오른쪽에 텍스트를 표시)
                        text = font.render(KEYPOINT_NAMES[i // 2], True, BLUE)
                        # screen.blit(text, (int(x) + 10, int(y) - 10))

                # 키포인트 좌표를 항상 기록 (0이든 아니든)
                keypoint_positions.append((x, y))

            # 이제 선을 그리기 (사람의 형태 만들기)
            
            # 왼쪽 팔꿈치와 왼쪽 어깨 연결
            if len(keypoint_positions) > 7 and len(keypoint_positions) > 5:
                if keypoint_positions[7][0] != 0 and keypoint_positions[7][1] != 0 and keypoint_positions[5][0] != 0 and keypoint_positions[5][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[7][0], keypoint_positions[7][1]), (keypoint_positions[5][0], keypoint_positions[5][1]), 2)

            # 왼쪽 팔꿈치와 왼쪽 손목 연결
            if len(keypoint_positions) > 7 and len(keypoint_positions) > 9:
                if keypoint_positions[7][0] != 0 and keypoint_positions[7][1] != 0 and keypoint_positions[9][0] != 0 and keypoint_positions[9][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[7][0], keypoint_positions[7][1]), (keypoint_positions[9][0], keypoint_positions[9][1]), 2)

            # 오른쪽 팔꿈치와 오른쪽 어깨 연결
            if len(keypoint_positions) > 8 and len(keypoint_positions) > 6:
                if keypoint_positions[8][0] != 0 and keypoint_positions[8][1] != 0 and keypoint_positions[6][0] != 0 and keypoint_positions[6][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[8][0], keypoint_positions[8][1]), (keypoint_positions[6][0], keypoint_positions[6][1]), 2)

            # 오른쪽 팔꿈치와 오른쪽 손목 연결
            if len(keypoint_positions) > 8 and len(keypoint_positions) > 10:
                if keypoint_positions[8][0] != 0 and keypoint_positions[8][1] != 0 and keypoint_positions[10][0] != 0 and keypoint_positions[10][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[8][0], keypoint_positions[8][1]), (keypoint_positions[10][0], keypoint_positions[10][1]), 2)

            # 왼쪽 무릎과 왼쪽 발목 연결
            if len(keypoint_positions) > 13 and len(keypoint_positions) > 15:
                if keypoint_positions[13][0] != 0 and keypoint_positions[13][1] != 0 and keypoint_positions[15][0] != 0 and keypoint_positions[15][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[13][0], keypoint_positions[13][1]), (keypoint_positions[15][0], keypoint_positions[15][1]), 2)

            # 오른쪽 무릎과 오른쪽 발목 연결
            if len(keypoint_positions) > 14 and len(keypoint_positions) > 16:
                if keypoint_positions[14][0] != 0 and keypoint_positions[14][1] != 0 and keypoint_positions[16][0] != 0 and keypoint_positions[16][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[14][0], keypoint_positions[14][1]), (keypoint_positions[16][0], keypoint_positions[16][1]), 2)

            # 몸통 선 (왼쪽 어깨 - 오른쪽 어깨)
            if len(keypoint_positions) > 5 and len(keypoint_positions) > 6:
                if keypoint_positions[5][0] != 0 and keypoint_positions[5][1] != 0 and keypoint_positions[6][0] != 0 and keypoint_positions[6][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[5][0], keypoint_positions[5][1]), (keypoint_positions[6][0], keypoint_positions[6][1]), 2)
                  
            # 왼쪽 어깨와 오른쪽 어깨를 이용해 수직 원 그리기
            if len(keypoint_positions) > 5 and len(keypoint_positions) > 6:
                left_shoulder = (keypoint_positions[5][0], keypoint_positions[5][1])
                right_shoulder = (keypoint_positions[6][0], keypoint_positions[6][1])

                if left_shoulder[0] != 0 and left_shoulder[1] != 0 and right_shoulder[0] != 0 and right_shoulder[1] != 0:
                    draw_perpendicular_circle(screen, left_shoulder, right_shoulder, GREEN)

                    
            # 왼쪽 엉덩이와 오른쪽 엉덩이 연결
            if len(keypoint_positions) > 11 and len(keypoint_positions) > 12:
                if keypoint_positions[11][0] != 0 and keypoint_positions[11][1] != 0 and keypoint_positions[12][0] != 0 and keypoint_positions[12][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[11][0], keypoint_positions[11][1]), (keypoint_positions[12][0], keypoint_positions[12][1]), 2)
                
            # 왼쪽 어깨 - 왼쪽 엉덩이 연결
            if len(keypoint_positions) > 5 and len(keypoint_positions) > 11:
                if keypoint_positions[5][0] != 0 and keypoint_positions[5][1] != 0 and keypoint_positions[11][0] != 0 and keypoint_positions[11][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[5][0], keypoint_positions[5][1]), (keypoint_positions[11][0], keypoint_positions[11][1]), 2)
                
            # 오른쪽 어깨 - 오른쪽 엉덩이 연결
            if len(keypoint_positions) > 6 and len(keypoint_positions) > 12:
                if keypoint_positions[6][0] != 0 and keypoint_positions[6][1] != 0 and keypoint_positions[12][0] != 0 and keypoint_positions[12][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[6][0], keypoint_positions[6][1]), (keypoint_positions[12][0], keypoint_positions[12][1]), 2)

            # 다리 연결 (왼쪽 엉덩이 - 왼쪽 무릎 - 왼쪽 발목)
            if len(keypoint_positions) > 11 and len(keypoint_positions) > 13 and len(keypoint_positions) > 15:
                if keypoint_positions[11][0] != 0 and keypoint_positions[11][1] != 0 and keypoint_positions[13][0] != 0 and keypoint_positions[13][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[11][0], keypoint_positions[11][1]), (keypoint_positions[13][0], keypoint_positions[13][1]), 2)
                if keypoint_positions[13][0] != 0 and keypoint_positions[13][1] != 0 and keypoint_positions[15][0] != 0 and keypoint_positions[15][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[13][0], keypoint_positions[13][1]), (keypoint_positions[15][0], keypoint_positions[15][1]), 2)

            # 다리 연결 (오른쪽 엉덩이 - 오른쪽 무릎 - 오른쪽 발목)
            if len(keypoint_positions) > 12 and len(keypoint_positions) > 14 and len(keypoint_positions) > 16:
                if keypoint_positions[12][0] != 0 and keypoint_positions[12][1] != 0 and keypoint_positions[14][0] != 0 and keypoint_positions[14][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[12][0], keypoint_positions[12][1]), (keypoint_positions[14][0], keypoint_positions[14][1]), 2)
                if keypoint_positions[14][0] != 0 and keypoint_positions[14][1] != 0 and keypoint_positions[16][0] != 0 and keypoint_positions[16][1] != 0:
                    pygame.draw.line(screen, GREEN, (keypoint_positions[14][0], keypoint_positions[14][1]), (keypoint_positions[16][0], keypoint_positions[16][1]), 2)

        # 화면을 OpenCV로 캡처하여 동영상에 추가
        video_frame = pygame.surfarray.array3d(pygame.display.get_surface())  # Pygame 화면을 OpenCV 형식으로 변환
        video_frame = video_frame.swapaxes(0, 1)  # 차원 변경 (Pygame은 (높이, 너비, 색상) 순서이고 OpenCV는 (너비, 높이, 색상) 순서)
        output_video.write(video_frame)  # 동영상에 프레임 추가

        # 화면 업데이트
        pygame.display.flip()

        # 한 프레임을 1초간 기다리기
        clock.tick(25)  # 초당 25 프레임
        
        # 다음 프레임으로 이동
        current_frame += 1
        if current_frame >= len(keypoints_data):
            running = False  # 모든 프레임을 다 보여주고 종료

    # Pygame 종료
    pygame.quit()
    output_video.release()  # 동영상 저장 종료

# 애니메이션 실행
animate_keypoints()
