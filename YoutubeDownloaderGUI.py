import os
import sys
import threading
import subprocess
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QRadioButton, QPushButton, QFileDialog,
                             QProgressBar, QButtonGroup, QGroupBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QDesktopServices, QCursor
from PyQt5.QtCore import QUrl
import yt_dlp


class DownloadWorker(QObject):
    """다운로드 작업을 처리하는 워커 클래스"""
    progress_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, url, media_type, audio_format, output_path):
        super().__init__()
        self.url = url
        self.media_type = media_type
        self.audio_format = audio_format
        self.output_path = output_path

    def progress_hook(self, d):
        """다운로드 진행 상황 업데이트"""
        self.progress_signal.emit(d)

    def run(self):
        """다운로드 실행"""
        try:
            # 출력 경로가 존재하는지 확인
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

            # 파일 이름 형식 설정 (경로 + 비디오 제목 + 확장자)
            output_template = os.path.join(self.output_path, '%(title)s.%(ext)s')

            # 미디어 유형에 따른 옵션 설정
            if self.media_type == 'video':
                # 비디오 다운로드 옵션
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': output_template,
                    'progress_hooks': [self.progress_hook],
                }
                final_ext = 'mp4'
            else:  # 오디오 다운로드 옵션
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': self.audio_format,
                        'preferredquality': '192',
                    }],
                    'outtmpl': output_template,
                    'progress_hooks': [self.progress_hook],
                }
                final_ext = self.audio_format

            # 다운로드 시작
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                video_title = info.get('title', 'video')
                downloaded_file = os.path.join(self.output_path, f"{video_title}.{final_ext}")

            self.finished_signal.emit(downloaded_file)

        except Exception as e:
            self.error_signal.emit(str(e))


class YoutubeDownloaderApp(QMainWindow):
    """유튜브 다운로더 GUI 애플리케이션"""

    def __init__(self):
        super().__init__()
        self.completed_file_path = None
        self.initUI()

    def initUI(self):
        """UI 초기화"""
        self.setWindowTitle('유튜브 다운로더')
        self.setGeometry(300, 300, 500, 300)

        # 메인 위젯과 레이아웃
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # URL 입력
        url_layout = QHBoxLayout()
        url_label = QLabel('유튜브 URL:')
        self.url_input = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # 미디어 타입 선택
        media_group_box = QGroupBox('다운로드 유형')
        media_layout = QHBoxLayout()

        self.media_group = QButtonGroup(self)
        self.video_radio = QRadioButton('영상 (MP4)')
        self.audio_radio = QRadioButton('소리')
        self.media_group.addButton(self.video_radio, 1)
        self.media_group.addButton(self.audio_radio, 2)
        self.video_radio.setChecked(True)

        media_layout.addWidget(self.video_radio)
        media_layout.addWidget(self.audio_radio)
        media_group_box.setLayout(media_layout)
        main_layout.addWidget(media_group_box)

        # 오디오 형식 선택 (오디오를 선택한 경우에만)
        audio_format_group_box = QGroupBox('오디오 형식')
        audio_format_layout = QHBoxLayout()

        self.audio_format_group = QButtonGroup(self)
        self.wav_radio = QRadioButton('WAV')
        self.mp3_radio = QRadioButton('MP3')
        self.audio_format_group.addButton(self.wav_radio, 1)
        self.audio_format_group.addButton(self.mp3_radio, 2)
        self.wav_radio.setChecked(True)

        audio_format_layout.addWidget(self.wav_radio)
        audio_format_layout.addWidget(self.mp3_radio)
        audio_format_group_box.setLayout(audio_format_layout)
        main_layout.addWidget(audio_format_group_box)

        # 저장 경로 선택
        path_layout = QHBoxLayout()
        path_label = QLabel('저장 경로:')
        self.path_input = QLineEdit()
        self.path_input.setText(os.path.join(os.getcwd(), 'outputs'))
        browse_button = QPushButton('찾아보기')
        browse_button.clicked.connect(self.browse_folder)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        main_layout.addLayout(path_layout)

        # 진행 상황 표시
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # 상태 라벨
        self.status_label = QLabel('준비됨')
        main_layout.addWidget(self.status_label)

        # 다운로드 버튼
        self.download_button = QPushButton('다운로드')
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)

        # 깃허브 링크 추가 (우측 정렬)
        github_link = QLabel('<a href="https://github.com/PriuS2/YoutubeDownloader">Github link</a>')
        github_link.setAlignment(Qt.AlignRight)
        github_link.setOpenExternalLinks(True)
        github_link.setCursor(QCursor(Qt.PointingHandCursor))
        main_layout.addWidget(github_link)

        # 미디어 타입에 따라 오디오 형식 옵션 활성화/비활성화
        self.video_radio.toggled.connect(self.toggle_audio_format_options)
        self.toggle_audio_format_options()

    def toggle_audio_format_options(self):
        """미디어 타입에 따라 오디오 형식 옵션 활성화/비활성화"""
        is_audio_selected = self.audio_radio.isChecked()
        self.wav_radio.setEnabled(is_audio_selected)
        self.mp3_radio.setEnabled(is_audio_selected)

    def browse_folder(self):
        """폴더 선택 다이얼로그 표시"""
        folder = QFileDialog.getExistingDirectory(self, '저장할 폴더 선택', os.getcwd())
        if folder:
            self.path_input.setText(folder)

    def start_download(self):
        """다운로드 시작"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '경고', '유튜브 URL을 입력해주세요.')
            return

        # 다운로드 파라미터 설정
        media_type = 'video' if self.video_radio.isChecked() else 'audio'
        audio_format = 'wav' if self.wav_radio.isChecked() else 'mp3'
        output_path = self.path_input.text()

        # 다운로드 워커 생성 및 시그널 연결
        self.worker = DownloadWorker(url, media_type, audio_format, output_path)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.download_finished)
        self.worker.error_signal.connect(self.download_error)

        # 다운로드 시작
        self.status_label.setText('다운로드 중...')
        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)

        # 쓰레드에서 다운로드 실행
        self.thread = threading.Thread(target=self.worker.run)
        self.thread.daemon = True
        self.thread.start()

    def update_progress(self, progress_data):
        """다운로드 진행 상황 업데이트"""
        if progress_data['status'] == 'downloading':
            # 기본 진행 정보
            status_text = '다운로드 중...'
            percentage = 0

            # 총 바이트 정보가 있는 경우 퍼센트 계산
            if 'total_bytes' in progress_data and progress_data['total_bytes'] > 0:
                percentage = int(progress_data['downloaded_bytes'] / progress_data['total_bytes'] * 100)
                status_text = f'{status_text} {percentage}%'
                self.progress_bar.setValue(percentage)

                # 다운로드 크기 표시 (MB 단위)
                total_mb = progress_data['total_bytes'] / (1024 * 1024)
                downloaded_mb = progress_data['downloaded_bytes'] / (1024 * 1024)
                status_text = f'{status_text} ({downloaded_mb:.2f}MB / {total_mb:.2f}MB)'

            # 속도 계산 (바이트/초 -> MB/s로 변환)
            speed = progress_data.get('speed', 0)
            if speed:
                speed_str = f"{speed / 1024 / 1024:.2f} MB/s"
                status_text = f'{status_text}, 속도: {speed_str}'

            # 남은 시간 계산
            eta = progress_data.get('eta', None)
            if eta is not None:
                # 초 단위의 eta를 분:초 형식으로 변환
                minutes, seconds = divmod(eta, 60)
                eta_str = f"{int(minutes)}분 {int(seconds)}초"
                status_text = f'{status_text}, 남은 시간: {eta_str}'

            # Fragment 정보 추가 (콘솔과 유사하게)
            fragment_info = ''
            if 'fragment_index' in progress_data and 'fragment_count' in progress_data:
                fragment_info = f" (조각 {progress_data['fragment_index']}/{progress_data['fragment_count']})"
                status_text = f'{status_text}{fragment_info}'

            # 상태 레이블 업데이트
            self.status_label.setText(status_text)

    def download_finished(self, file_path):
        """다운로드 완료 처리"""
        self.progress_bar.setValue(100)
        self.status_label.setText(f'다운로드 완료: {os.path.basename(file_path)}')
        self.download_button.setEnabled(True)

        # 다운로드 완료 메시지 박스에 열기 버튼과 폴더 열기 버튼 추가
        self.completed_file_path = file_path
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('완료')
        msg_box.setText(f'다운로드가 완료되었습니다.\n파일: {file_path}')
        msg_box.setStandardButtons(QMessageBox.Ok)
        open_button = msg_box.addButton('파일 열기', QMessageBox.ActionRole)
        open_folder_button = msg_box.addButton('폴더 열기', QMessageBox.ActionRole)
        msg_box.exec_()

        # 버튼에 따른 동작 처리
        clicked_button = msg_box.clickedButton()
        if clicked_button == open_button:
            self.open_file(file_path)
        elif clicked_button == open_folder_button:
            self.open_folder(os.path.dirname(file_path))

    def download_error(self, error_msg):
        """다운로드 오류 처리"""
        self.status_label.setText(f'오류 발생: {error_msg}')
        self.download_button.setEnabled(True)
        QMessageBox.critical(self, '오류', f'다운로드 중 오류가 발생했습니다:\n{error_msg}')

    def open_file(self, file_path):
        """다운로드된 파일 열기"""
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux
                subprocess.call(['xdg-open', file_path])
            self.status_label.setText(f'파일 열기: {os.path.basename(file_path)}')
        except Exception as e:
            QMessageBox.warning(self, '경고', f'파일을 열 수 없습니다:\n{str(e)}')

    def open_folder(self, folder_path):
        """다운로드된 파일이 있는 폴더 열기"""
        try:
            if platform.system() == 'Windows':
                os.startfile(folder_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', folder_path])
            else:  # Linux
                subprocess.call(['xdg-open', folder_path])
            self.status_label.setText(f'폴더 열기: {os.path.basename(folder_path)}')
        except Exception as e:
            QMessageBox.warning(self, '경고', f'폴더를 열 수 없습니다:\n{str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YoutubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
