import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

class Animater:
    def __init__(self, data):
        self.__data = data
    
    def set_data(self, data):
        self.__data = data

    def bind_gif(self, path1, path2):
        image1_path = path1
        image2_path = path2

        # 画像を開く
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)

        # 画像の幅と高さを取得
        width1, height1 = image1.size
        width2, height2 = image2.size

        new_width = width1 + width2
        new_height = max(height1, height2)  

        # 画像を横に並べるための新しい画像リストを作成
        combined_frames = []

        # アニメーションの各フレームにアクセスし、新しい画像リストに追加
        num_frames = min(len(image1.seek(0)), len(image2.seek(0)))
        for i in range(num_frames):
            image1.seek(i)
            frame1 = image1.copy()
            image2.seek(i)
            frame2 = image2.copy()
            
            combined_frame = Image.new("RGBA", (new_width, new_height))
            combined_frame.paste(frame1, (0, 0))
            combined_frame.paste(frame2, (width1, 0))
            combined_frames.append(combined_frame)

        # 新しいGIF画像を保存（アニメーションを保持）
        combined_frames[0].save(
            "animated_combined.gif",
            save_all=True,
            append_images=combined_frames[1:],  # 最初のフレームを除く
            duration=image1.info["duration"],  # 最初のGIFの表示時間を使用
            loop=0  # 無限ループ（0は無限ループ）
        )


    def generate_gif(self, path):

        def __update(frame):
            x, y = self.__data[frame]
            trajectory_data.append([x, y])  # 現在の座標を軌跡データに追加
            point.set_data(x, y)
            trajectory.set_data(*zip(*trajectory_data))  # 軌跡を更新
            
            # ループしたら軌跡データをクリア
            if frame == len(self.__data) - 1:
                trajectory_data.clear()
            
            return point, trajectory
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        # プロットを初期化
        point, = ax.plot([], [], 'ro') 
        trajectory, = ax.plot([], [], 'b-') 

        # 点の軌跡を保存するリスト
        trajectory_data = []

        # アニメーションの設定
        ani = FuncAnimation(fig, __update, frames=len(self.__data), blit=True, interval=300)

        # GIFファイルとして保存
        ani.save(path, writer="pillow")

        plt.show()