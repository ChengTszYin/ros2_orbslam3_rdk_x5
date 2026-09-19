# orbslam_stereo_compress.launch.py
import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # folder where you used to run: ros2 run orb_slam3_example_ros2 stereo ./src/...
    ws = os.path.expanduser('~/ros2_ws')   # change if your workspace path is different

    voc = os.path.join(ws, 'src/orb_slam3/ORB_SLAM3/Vocabulary/ORBvoc.txt')
    yaml = os.path.join(ws, 'src/orb_slam3/ORB_SLAM3/Examples/Stereo/OAK_D_Lite.yaml')

    orbslam = Node(
        package='orb_slam3_example_ros2',
        executable='stereo',
        name='orbslam3_stereo',
        output='screen',
        arguments=[
            voc,
            yaml,
            'true',
        ],
        remappings=[
            ('/oak/left/image_raw', '/camera/camera/infra1/image_rect_raw'),
            ('/oak/right/image_raw', '/camera/camera/infra2/image_rect_raw'),
        ],
    )

    compress_keypoints = Node(
        package='image_transport',
        executable='republish',
        name='compress_keypoint_render',
        output='screen',
        arguments=['raw', 'compressed'],
        remappings=[
            ('in', '/keypoint_render_frame'),
            ('out', '/orbslam_render_frame'),
        ],
    )

    return LaunchDescription([
        orbslam,
        compress_keypoints,
    ])
