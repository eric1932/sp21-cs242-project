import * as React from 'react';
import {StyleSheet, TouchableHighlight} from 'react-native';
import {View} from '../components/Themed';
import {getTemplateList} from "../utils/API";
import MyProfileItem from "../components/MyProfileItem";
import {Entypo} from "@expo/vector-icons";

export default function TaskScreen() {
  let [templateList, setTemplateList] = React.useState<Array<string>>([])

  React.useEffect(() => {
    getTemplateList().then((result: Array<string>) => {
      setTemplateList([...templateList, ...result])
    })
  }, [])

  return (
    <View style={styles.container}>
      {templateList.map((eachTemplate: string) => (
        <MyProfileItem key={eachTemplate} name={eachTemplate} value={(
          <TouchableHighlight onPress={() => {
            console.warn('asdf')
          }}>
            <Entypo name="plus" size={24} color="black" />
          </TouchableHighlight>
        )} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    // justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
