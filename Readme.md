# 유튜브 다운로더 (YouTube Downloader)

PyQt5로 구현된 심플하고 직관적인 유튜브 동영상/오디오 다운로더 애플리케이션입니다.

## 주요 기능

- 유튜브 URL을 통한 간편한 다운로드
- 비디오(MP4) 또는 오디오(MP3, WAV) 형식 선택 가능
- 다운로드 진행률, 속도, 예상 시간 실시간 표시
- 사용자 지정 저장 경로 설정
- 다운로드 완료 후 파일 바로 열기 기능
- 크로스 플랫폼 지원 (Windows, macOS, Linux)

## 설치 방법

### Portable exe
[Release](https://github.com/PriuS2/YoutubeDownloader/releases)

### 요구 사항

- Python 3.6 이상
- PyQt5
- yt-dlp
- FFmpeg (오디오 변환 시 필요)

### 패키지 설치

```bash
# 필수 라이브러리 설치
pip install PyQt5 yt-dlp
```

### FFmpeg 설치

오디오 다운로드 기능을 사용하려면 FFmpeg가 필요합니다:

- **Windows**: [FFmpeg 공식 사이트](https://www.ffmpeg.org/download.html)에서 다운로드 후 PATH에 추가 or 동일경로에 압축풀기
  
## 사용 방법

1. 애플리케이션 실행:
   ```bash
   python youtube_downloader.py
   ```

2. 유튜브 영상 URL 입력

3. 원하는 다운로드 유형 선택 (비디오 또는 오디오)
   - 오디오 선택 시 MP3 또는 WAV 형식 중 선택 가능

4. 저장 경로 설정 (기본값: 현재 작업 디렉토리의 'outputs' 폴더)

5. '다운로드' 버튼 클릭

6. 다운로드 완료 후 '파일 열기' 버튼으로 결과물 바로 확인 가능

## 코드 구조

- `DownloadWorker` 클래스: 백그라운드에서 다운로드 작업을 관리하고 진행 상황을 메인 UI에 전달
- `YoutubeDownloaderApp` 클래스: 메인 애플리케이션 및 GUI 인터페이스 구현

## 라이선스

MIT License

## 기여하기

이슈 또는 풀 리퀘스트를 통해 프로젝트 개선에 기여해주세요.

## 주의사항

- 항상 저작권을 존중하고 개인 용도로만 사용해주세요.
- 유튜브 서비스 약관을 준수하는 범위 내에서 사용해주세요.
