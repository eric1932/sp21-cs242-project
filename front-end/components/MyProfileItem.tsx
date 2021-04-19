import React from "react";
import {Text, View} from "./Themed";
import {MyProfileItemProps} from "../types";

export default function MyProfileItem(props: MyProfileItemProps) {
  return (
    <View>
      <Text>{props.name}</Text>
      <Text>{props.value}</Text>
    </View>
  )
}