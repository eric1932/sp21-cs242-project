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
  TabOne: undefined;
  My: undefined;
};

export type TabOneParamList = {
  TabOneScreen: undefined;
};

export type TabTwoParamList = {
  My: undefined;
};

export type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Login'>;
export type LoginProps = {
  navigation: LoginScreenNavigationProp
}

export type MyProfileItemProps = {
  name: string,
  value: string,
}
