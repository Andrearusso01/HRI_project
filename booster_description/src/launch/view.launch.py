#!/usr/bin/env -S ros2 launch
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue 
def generate_launch_description():
    
    # --- CONFIGURAZIONE ---
    # Sostituisci con il nome reale del tuo pacchetto ROS2
    package_name = 'booster_description' 
    # Sostituisci con il nome del file che hai salvato nella cartella urdf/
    urdf_file_name = 'T1_23dof.urdf' 

    # --- ARGOMENTI DI LANCIO ---
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    # Argomento per abilitare/disabilitare il tempo simulato
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # --- PERCORSI E DESCRIZIONE ROBOT ---
    pkg_share = FindPackageShare(package_name)
    
    # Costruisce il percorso al file URDF: share_folder/urdf/t1.urdf
    urdf_model_path = PathJoinSubstitution([pkg_share, 'urdf', urdf_file_name])

    # Legge l'URDF usando xacro (funziona anche con file .urdf standard)
    robot_description_content = ParameterValue(Command(['xacro ', urdf_model_path]), value_type=str)
    
    robot_description = {'robot_description': robot_description_content}

    # --- NODI ---
    
    # 1. Robot State Publisher: Pubblica la struttura statica del robot (TF)
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': use_sim_time}]
    )

    # 2. Joint State Publisher GUI: Apre una finestrella con gli slider per muovere i giunti
    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # 3. RViz2: Il visualizzatore 3D
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # Se hai un file di configurazione .rviz salvato, puoi aggiungerlo qui negli arguments
        # arguments=['-d', PathJoinSubstitution([pkg_share, 'rviz', 'config.rviz'])]
    )

    # --- RITORNO DELLA DESCRIZIONE ---
    return LaunchDescription([
        declare_use_sim_time,
        node_robot_state_publisher,
        node_joint_state_publisher_gui,
        node_rviz
    ])