/**
 * Learn more about using TypeScript with React Navigation:
 * https://reactnavigation.org/docs/typescript/
 */
import {StackNavigationProp} from "@react-navigation/stack";
import {Component, ReactElement} from "react";

export type RootStackParamList = {
  Login: undefined;
  Root: undefined;
  NotFound: undefined;
};

export type BottomTabParamList = {
  Tasks: undefined;
  Templates: undefined;
  My: undefined;
};

export type TaskParamList = {
  TaskScreen: undefined;
};

export type TemplateParamList = {
  Template: undefined;
}

export type MyProfileParamList = {
  MyProfile: undefined;
  Login: undefined;
};

export type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Login'>;
export type LoginProps = {
  navigation: LoginScreenNavigationProp
}

export type MyProfileItemProps = {
  name: string,
  value: string | Component | ReactElement,
}

export type MyProfileScreenNavigationProp = StackNavigationProp<MyProfileParamList, 'MyProfile'>
export type MyProfileProps = {
  navigation: MyProfileScreenNavigationProp
}

export type TemplateScreenNavigationProp = StackNavigationProp<TemplateParamList, 'Template'>
export type TemplateProps = {
  navigation: TemplateScreenNavigationProp
}
