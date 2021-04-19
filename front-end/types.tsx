/**
 * Learn more about using TypeScript with React Navigation:
 * https://reactnavigation.org/docs/typescript/
 */
import {StackNavigationProp} from "@react-navigation/stack";

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
  TemplateScreen: undefined;
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
  value: string,
}

export type MyProfileScreenNavigationProp = StackNavigationProp<MyProfileParamList, 'MyProfile'>
export type MyProfileProps = {
  navigation: MyProfileScreenNavigationProp
}
