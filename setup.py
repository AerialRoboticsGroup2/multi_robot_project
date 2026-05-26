from setuptools import setup

package_name = 'multi_robot_project'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@email.com',
    description='Multi robot cooperative control',
    license='MIT',
    entry_points={
        'console_scripts': [
            'formation_controller = scripts.formation_controller:main',
            'collision_avoidance = scripts.collision_avoidance:main',
            'coverage_controller = scripts.coverage_controller:main',
            'consensus_node = scripts.consensus_node:main',
            'lidar_processor = scripts.lidar_processor:main',
            'connectivity_monitor = scripts.connectivity_monitor:main',
        ],
    },
)
