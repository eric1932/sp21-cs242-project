/**
 * Learn more about createBottomTabNavigator:
 * https://reactnavigation.org/docs/bottom-tab-navigator
 */

import {AntDesign, Feather, FontAwesome5, Ionicons} from '@expo/vector-icons';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createStackNavigator} from '@react-navigation/stack';
import * as React from 'react';

import Colors from '../constants/Colors';
import useColorScheme from '../hooks/useColorScheme';
import TaskScreen from '../screens/TaskScreen';
import MyProfileScreen from '../screens/MyProfileScreen';
import {BottomTabParamList, MyProfileParamList, TaskParamList, TemplateParamList} from '../types';
import TemplateScreen from "../screens/TemplateScreen";

const BottomTab = createBottomTabNavigator<BottomTabParamList>();

export default function BottomTabNavigator() {
  const colorScheme = useColorScheme();

  return (
    <BottomTab.Navigator
      initialRouteName="Tasks"
      tabBarOptions={{activeTintColor: Colors[colorScheme].tint}}>
      <BottomTab.Screen
        name="Tasks"
        component={TasksNavigator}
        options={{
          tabBarIcon: ({color}) => <FontAwesome5 name="tasks" size={24} color={color}/>,
        }}
      />
      <BottomTab.Screen
        name="Templates"
        component={TemplateNavigator}
        options={{
          tabBarIcon: ({color}) => <AntDesign name="plussquareo" size={24} color={color}/>,
        }}
      />
      <BottomTab.Screen
        name="My"
        component={MyProfileNavigator}
        options={{
          tabBarIcon: ({color}) => <Feather name="settings" size={24} color={color}/>,
        }}
      />
    </BottomTab.Navigator>
  );
}

// You can explore the built-in icon families and icons on the web at:
// https://icons.expo.fyi/

// Each tab has its own navigation stack, you can read more about this pattern here:
// https://reactnavigation.org/docs/tab-based-navigation#a-stack-navigator-for-each-tab
const TaskStack = createStackNavigator<TaskParamList>();

function TasksNavigator() {
  return (
    <TaskStack.Navigator>
      <TaskStack.Screen
        name="TaskScreen"
        component={TaskScreen}
        options={{
          headerTitle: 'Tasks',
          headerRight: ({tintColor}) => (
            <Ionicons
              name="refresh"
              size={24}
              color={tintColor}
              style={{paddingRight: 20}}
              onPress={() => window.location.reload()} />
          )
        }}
      />
    </TaskStack.Navigator>
  );
}

const TemplateStack = createStackNavigator<TemplateParamList>();

function TemplateNavigator() {
  return (
    <TemplateStack.Navigator>
      <TemplateStack.Screen
        name="Template"
        component={TemplateScreen}
        options={{headerTitle: 'Templates'}}
      />
    </TemplateStack.Navigator>
  )
}

const MyProfileStack = createStackNavigator<MyProfileParamList>();

function MyProfileNavigator() {
  return (
    <MyProfileStack.Navigator>
      <MyProfileStack.Screen
        name="MyProfile"
        component={MyProfileScreen}
        options={{headerTitle: 'My'}}
      />
    </MyProfileStack.Navigator>
  );
}
