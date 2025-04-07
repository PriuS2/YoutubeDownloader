# YouTube Audio Downloader

이 프로젝트는 YouTube 동영상에서 오디오만 추출하여 다운로드하는 간단한 Python 스크립트입니다.

## 주요 기능

- YouTube URL에서 최고 품질의 오디오 추출
- WAV 형식으로 변환
- 다운로드 경로 지정 가능
- 간단한 명령줄 인터페이스

## 설치 방법

1. 이 저장소를 클론합니다:
```bash
git clone https://github.com/your-username/youtube-audio-downloader.git
cd youtube-audio-downloader
```

2. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

## 필수 패키지

- yt-dlp
- FFmpeg (외부 종속성)

## 사용 방법

### 스크립트 직접 실행

```bash
python youtube_audio_downloader.py
```

실행 후 프롬프트에 YouTube URL을 입력하면 `./outputs` 디렉토리에 오디오 파일이 다운로드됩니다.

### 코드에서 함수 임포트

```python
from youtube_audio_downloader import download_audio

# URL에서 오디오 다운로드
url = "https://www.youtube.com/watch?v=example"
output_path = "./my_music"
downloaded_file = download_audio(url, output_path)

print(f"파일이 다운로드되었습니다: {downloaded_file}")
```

## 함수 설명

```python
download_audio(url, output_path=None)
```

### 매개변수:
- `url` (str): 유튜브 비디오 URL
- `output_path` (str, optional): 다운로드 경로. 기본값은 현재 디렉토리입니다.

### 반환값:
- `str`: 다운로드된 파일 경로 또는 오류 발생 시 None

## 주의사항

- 이 스크립트를 사용하기 전에 YouTube 이용약관을 확인하세요.
- 저작권이 있는 콘텐츠는 개인 용도로만 다운로드하세요.
- FFmpeg가 시스템에 설치되어 있어야 합니다.

## FFmpeg 설치 방법

### Windows
1. [FFmpeg 웹사이트](https://ffmpeg.org/download.html)에서 Windows 빌드를 다운로드합니다.
2. 압축을 풀고 PATH 환경 변수에 추가합니다.

### macOS
```bash
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

## 라이센스

MIT

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새 기능 브랜치를 만듭니다 (`git checkout -b feature/amazing-feature`).
3. 변경사항을 커밋합니다 (`git commit -m '새로운 기능 추가'`).
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`).
5. Pull Request를 제출합니다.
