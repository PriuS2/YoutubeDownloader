import os
import yt_dlp


def download_audio(url, output_path=None):
    """
    yt-dlp를 사용하여 유튜브 URL에서 오디오만 다운로드합니다.

    매개변수:
        url (str): 유튜브 비디오 URL
        output_path (str, optional): 다운로드 경로. 기본값은 현재 디렉토리입니다.

    반환:
        str: 다운로드된 파일 경로
    """
    try:
        # 기본 다운로드 경로 설정
        if output_path is None:
            output_path = os.getcwd()

        # 출력 경로가 존재하는지 확인
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # 파일 이름 형식 설정 (경로 + 비디오 제목 + 확장자)
        output_template = os.path.join(output_path, '%(title)s.%(ext)s')

        # yt-dlp 옵션 설정
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
        }

        # 다운로드 시작
        print(f"다운로드 중: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            downloaded_file = os.path.join(output_path, f"{video_title}.wav")

        print(f"다운로드 완료: {downloaded_file}")
        return downloaded_file

    except Exception as e:
        print(f"다운로드 중 오류 발생: {str(e)}")
        return None


# 사용 예시
if __name__ == "__main__":
    video_url = input("유튜브 URL을 입력하세요: ")
    # save_path = input("저장 경로를 입력하세요 (기본: 현재 디렉토리): ")
    #
    # if not save_path:
    #     save_path = None

    save_path = '.\outputs'
    download_audio(video_url, save_path)

    pause = input("완료! 종료하려면 Enter을 누르시오.")
