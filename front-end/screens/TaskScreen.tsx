import * as React from 'react';
import {StyleSheet, Text, TouchableOpacity} from 'react-native';
import {View} from '../components/Themed';
import {deleteTask, listTasks} from "../utils/API";
import {getToken} from "../utils/Storage";
import {userTaskItem} from "../types";
import ListItem from "../components/ListItem";
import {AntDesign, Feather} from "@expo/vector-icons";
import {Dispatch} from "react";

function editTask(item: userTaskItem) {
  //
}

async function performDeleteTask(item: userTaskItem,
                                 index: number,
                                 showConfirmDelete: number,
                                 setShowConfirmDelete: Dispatch<number>,
                                 setUserTaskList: Dispatch<userTaskItem[]>) {
  if (index === showConfirmDelete) {
    // delete
    let token = await getToken()
    if (token) {
      await deleteTask(token, item)
    }
    // refresh
    let result = await listTasks(token ? token : '')
    setUserTaskList([...result])
    // reset state
    setShowConfirmDelete(-1)
  } else {
    // set confirm button
    setShowConfirmDelete(index)
  }
}

export default function TaskScreen() {
  let [userTaskList, setUserTaskList] = React.useState<userTaskItem[]>([])
  let [showDialog, setShowDialog] = React.useState(false)
  let [showConfirmDelete, setShowConfirmDelete] = React.useState(-1)

  React.useEffect(() => {
    getToken().then(token => {
      listTasks(token ? token : '').then(result => {
        setUserTaskList([...result])
      })
    })
  }, [])

  return (
    <View style={styles.container}>
      {userTaskList.map((item, index) => (
        <ListItem key={item.apscheduler_id.join('-')}
                  name={item.apscheduler_id.join('-') + (item.note === '' ? '' : (': ' + item.note))}
                  value={(
                    <View style={{flexDirection: 'row'}}>
                      <TouchableOpacity onPress={() => editTask(item)}>
                        <AntDesign name="edit" size={24} color="black"/>
                      </TouchableOpacity>
                      <TouchableOpacity onPress={
                        () => performDeleteTask(item, index, showConfirmDelete, setShowConfirmDelete, setUserTaskList)
                      }
                                        style={{marginLeft: 15}}>
                        {showConfirmDelete === index
                          ? <Text>Confirm</Text>
                          : <Feather name="trash" size={24} color="black"/>}
                      </TouchableOpacity>
                    </View>
                  )}/>)
      )}
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
