import React, {ReactElement} from "react";
import {Text} from "./Themed";
import {View} from "react-native";
import {MyProfileItemProps} from "../types";

export default function ListItem(props: MyProfileItemProps): ReactElement {
  return (
    <View style={{
      alignItems: 'center',
      borderBottomWidth: 1,
      borderColor: '#eee',
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between',
      width: '90%',
      marginLeft: '5%',
      marginRight: '5%',
      paddingVertical: 10,
      paddingHorizontal: 10,
    }}>
      <Text>{props.name}</Text>
      {props.value === null
        ? undefined
        : typeof props.value === 'string'
          ? <Text>{props.value}</Text>
          : props.value}
    </View>
  )
}