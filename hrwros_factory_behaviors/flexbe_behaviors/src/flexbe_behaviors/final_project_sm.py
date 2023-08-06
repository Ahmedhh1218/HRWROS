#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_manipulation_states.srdf_state_to_moveit import SrdfStateToMoveit as flexbe_manipulation_states__SrdfStateToMoveit
from flexbe_states.subscriber_state import SubscriberState
from hrwros_factory_states.compute_grasp_state import ComputeGraspState
from hrwros_factory_states.control_feeder_state import ControlFeederState
from hrwros_factory_states.detect_part_camera_state import DetectPartCameraState
from hrwros_factory_states.locate_factory_device_state import LocateFactoryDeviceState
from hrwros_factory_states.move_base_state import MoveBaseState as hrwros_factory_states__MoveBaseState
from hrwros_factory_states.moveit_to_joints_dyn_state import MoveitToJointsDynState as hrwros_factory_states__MoveitToJointsDynState
from hrwros_factory_states.set_conveyor_power_state import SetConveyorPowerState
from hrwros_factory_states.srdf_state_to_moveit import SrdfStateToMoveit as hrwros_factory_states__SrdfStateToMoveit
from hrwros_factory_states.vacuum_gripper_control_state import VacuumGripperControlState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]
from geometry_msgs.msg import Pose2D

# [/MANUAL_IMPORT]


'''
Created on 28/7/2023
@author: Ahmed Hassabou
'''
class FinalProjectSM(Behavior):
	'''
	Final project for the MOOC Hello (Real) World with ROS
The three robots in the factory move to process the parts
	'''


	def __init__(self):
		super(FinalProjectSM, self).__init__()
		self.name = 'Final Project'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		names1 = ['robot1_shoulder_pan_joint', 'robot1_shoulder_lift_joint', 'robot1_elbow_joint', 'robot1_wrist_1_joint', 'robot1_wrist_2_joint', 'robot1_wrist_3_joint']
		pick1_group = 'robot1'
		robot1_loc = Pose2D(x=3.8, y=2.1, theta=-90.0)
		gripper1 = "vacuum_gripper1_suction_cup"
		pick2_group = 'robot2'
		robot2_loc = Pose2D(x=-4.3, y=-0.9, theta=0.0)
		gripper2 = "vacuum_gripper2_suction_cup"
		names2 = ['robot2_shoulder_pan_joint', 'robot2_shoulder_lift_joint', 'robot2_elbow_joint', 'robot2_wrist_1_joint', 'robot2_wrist_2_joint', 'robot2_wrist_3_joint']
		# x:42 y:183, x:594 y:345
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.robot1_loc = robot1_loc
		_state_machine.userdata.pose_turtlebot = []
		_state_machine.userdata.pick1_configuration = []
		_state_machine.userdata.place1_configuration = []
		_state_machine.userdata.conveyor_speed = 100
		_state_machine.userdata.robot2_loc = robot2_loc
		_state_machine.userdata.pick2_configuration = []
		_state_machine.userdata.place2_configuration = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]


		with _state_machine:
			# x:32 y:103
			OperatableStateMachine.add('Move R1 Home',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R1Home', move_group=pick1_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'start conveyor', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:33 y:614
			OperatableStateMachine.add('Activate Gripper 2',
										VacuumGripperControlState(enable=True, service_name='/gripper2/control'),
										transitions={'continue': 'Move R2 to Pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1122 y:138
			OperatableStateMachine.add('Compute pick',
										ComputeGraspState(group=pick1_group, offset=0.0, joint_names=names1, tool_link=gripper1, rotation=3.1415),
										transitions={'continue': 'Activate Gripper 1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick1_configuration', 'joint_names': 'joint_names'})

			# x:1026 y:616
			OperatableStateMachine.add('Compute place Turtlebot',
										ComputeGraspState(group=pick1_group, offset=0.6, joint_names=names1, tool_link=gripper1, rotation=3.1415),
										transitions={'continue': 'Move R1 to place', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_turtlebot', 'joint_values': 'place1_configuration', 'joint_names': 'joint_names'})

			# x:93 y:710
			OperatableStateMachine.add('Compute second pick',
										ComputeGraspState(group=pick2_group, offset=0.0, joint_names=names2, tool_link=gripper2, rotation=3.1415),
										transitions={'continue': 'Activate Gripper 2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick2_configuration', 'joint_names': 'joint_names'})

			# x:862 y:775
			OperatableStateMachine.add('De-activate gripper 1',
										VacuumGripperControlState(enable=False, service_name='/gripper1/control'),
										transitions={'continue': 'Move R1 Back Home', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:24 y:236
			OperatableStateMachine.add('De-activate gripper 2',
										VacuumGripperControlState(enable=False, service_name='/gripper2/control'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1113 y:59
			OperatableStateMachine.add('Detect Part Camera',
										DetectPartCameraState(ref_frame='robot1_base', camera_topic='/hrwros/logical_camera_1', camera_frame='logical_camera_1_frame'),
										transitions={'continue': 'Compute pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:257 y:746
			OperatableStateMachine.add('Detect Part Camera 2',
										DetectPartCameraState(ref_frame='robot2_base', camera_topic='/hrwros/logical_camera_2', camera_frame='logical_camera_2_frame'),
										transitions={'continue': 'Compute second pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:1095 y:548
			OperatableStateMachine.add('LocateTurtlebot',
										LocateFactoryDeviceState(model_name='mobile_base', output_frame_id='world'),
										transitions={'succeeded': 'Compute place Turtlebot', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose_turtlebot'})

			# x:633 y:765
			OperatableStateMachine.add('Move R1 Back Home',
										hrwros_factory_states__SrdfStateToMoveit(config_name='R1Home', move_group=pick1_group, action_topic='/move_group', robot_name=""),
										transitions={'reached': 'Navigate to Robot 2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1125 y:370
			OperatableStateMachine.add('Move R1 back Home',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R1Home', move_group=pick1_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Navigate to Robot 1', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1121 y:278
			OperatableStateMachine.add('Move R1 to pick',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick1_group, offset=0.0, tool_link=gripper1, action_topic='/move_group'),
										transitions={'reached': 'Move R1 back Home', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick1_configuration', 'joint_names': 'joint_names'})

			# x:1039 y:693
			OperatableStateMachine.add('Move R1 to place',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick1_group, offset=0.0, tool_link=gripper1, action_topic='/move_group'),
										transitions={'reached': 'De-activate gripper 1', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'place1_configuration', 'joint_names': 'joint_names'})

			# x:16 y:429
			OperatableStateMachine.add('Move R2 back to Home',
										flexbe_manipulation_states__SrdfStateToMoveit(config_name='R2Home', move_group=pick2_group, action_topic='/move_group', robot_name=''),
										transitions={'reached': 'Move R2 to Bin', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:35 y:340
			OperatableStateMachine.add('Move R2 to Bin',
										hrwros_factory_states__SrdfStateToMoveit(config_name='R2Place', move_group=pick2_group, action_topic='/move_group', robot_name=""),
										transitions={'reached': 'De-activate gripper 2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'robot_name': 'robot_name', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:28 y:506
			OperatableStateMachine.add('Move R2 to Pick',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick2_group, offset=0.0, tool_link=gripper2, action_topic='/move_group'),
										transitions={'reached': 'Move R2 back to Home', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick2_configuration', 'joint_names': 'joint_names'})

			# x:1159 y:477
			OperatableStateMachine.add('Navigate to Robot 1',
										hrwros_factory_states__MoveBaseState(),
										transitions={'arrived': 'LocateTurtlebot', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'robot1_loc'})

			# x:449 y:771
			OperatableStateMachine.add('Navigate to Robot 2',
										hrwros_factory_states__MoveBaseState(),
										transitions={'arrived': 'Detect Part Camera 2', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'robot2_loc'})

			# x:381 y:59
			OperatableStateMachine.add('Start feeder',
										ControlFeederState(activation=True),
										transitions={'succeeded': 'Wait for part', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off})

			# x:718 y:59
			OperatableStateMachine.add('Stop feeder',
										ControlFeederState(activation=False),
										transitions={'succeeded': 'stop conveyor', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off})

			# x:556 y:60
			OperatableStateMachine.add('Wait for part',
										SubscriberState(topic='/break_beam_sensor_change', blocking=True, clear=True),
										transitions={'received': 'Stop feeder', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})

			# x:217 y:76
			OperatableStateMachine.add('start conveyor',
										SetConveyorPowerState(stop=False),
										transitions={'succeeded': 'Start feeder', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'speed': 'conveyor_speed'})

			# x:900 y:28
			OperatableStateMachine.add('stop conveyor',
										SetConveyorPowerState(stop=True),
										transitions={'succeeded': 'Detect Part Camera', 'failed': 'failed'},
										autonomy={'succeeded': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'speed': 'conveyor_speed'})

			# x:1106 y:208
			OperatableStateMachine.add('Activate Gripper 1',
										VacuumGripperControlState(enable=True, service_name='/gripper1/control'),
										transitions={'continue': 'Move R1 to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
