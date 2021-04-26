/**
 * Task Screen
 */
import * as React from 'react';
import {Dispatch, ReactElement} from 'react';
import {Button, StyleSheet, Text, TextInput, TouchableOpacity} from 'react-native';
import {View} from '../components/Themed';
import {deleteTask, listTasks, updateTaskNote} from "../utils/API";
import {getToken} from "../utils/Storage";
import {userTaskItem} from "../types";
import ListItem from "../components/ListItem";
import {AntDesign, Feather} from "@expo/vector-icons";

/**
 * Handle UI delete request
 * @param item the task to delete
 * @param index the index that is selected
 * @param showConfirmDelete the state of index of previously selected item
 * @param setShowConfirmDelete setter
 * @param setUserTaskList used to refresh deleted list
 */
async function performDeleteTask(item: userTaskItem,
                                 index: number,
                                 showConfirmDelete: number,
                                 setShowConfirmDelete: Dispatch<number>,
                                 setUserTaskList: Dispatch<userTaskItem[]>) {
  if (index === showConfirmDelete) {
    // delete
    const token = await getToken()
    if (token) {
      await deleteTask(token, item)
    }
    // refresh
    const result = await listTasks(token ? token : '')
    setUserTaskList([...result])
    // reset state
    setShowConfirmDelete(-1)
  } else {
    // set confirm button
    setShowConfirmDelete(index)
  }
}

/**
 * Handle UI edit request
 * @param setShowEditDialog set self visibility
 * @param setPeriod
 * @param setNote
 * @param setTargetTaskID
 * @param item the task to update
 */
function performEditTask(setShowEditDialog: Dispatch<boolean>,
                         setPeriod: Dispatch<string>,
                         setNote: Dispatch<string>,
                         setTargetTaskID: Dispatch<string>,
                         item: userTaskItem): () => void {
  return () => {

    setShowEditDialog(true)
    setPeriod(item.period.toString())
    setNote(item.note)
    setTargetTaskID(item.apscheduler_id.join('-'))
  };
}

export default function TaskScreen(): ReactElement {
  const [userTaskList, setUserTaskList] = React.useState<userTaskItem[]>([])
  const [showEditDialog, setShowEditDialog] = React.useState(false)
  const [showConfirmDelete, setShowConfirmDelete] = React.useState(-1)

  const [targetTaskID, setTargetTaskID] = React.useState('')
  const [updatedPeriod, setPeriod] = React.useState('')
  const [updatedNote, setNote] = React.useState('')

  React.useEffect(() => {
    void getToken().then(token => {
      void listTasks(token ? token : '').then(result => {
        setUserTaskList([...result])
      })
    })
  }, [])

  return (
    <View style={styles.container}>
      {showEditDialog
        ? (<View style={{width: '60%'}}>
          <Text>Edit: {targetTaskID}</Text>
          <Text>Period (in secs)</Text>
          <TextInput value={updatedPeriod} onChangeText={(text) => {
            setPeriod(text)
          }}/>
          <Text>Note</Text>
          <TextInput value={updatedNote} placeholder={'(empty)'} onChangeText={(text) => {
            setNote(text)
          }}/>
          <Text>Cookies</Text>
          <TextInput placeholder={'(empty)'}/>
          <Button title={'Update'} onPress={async () => {
            const token = await getToken()
            if (token) {
              await updateTaskNote(token, targetTaskID, updatedNote)
              // refresh
              const result = await listTasks(token ? token : '')
              setUserTaskList([...result])
              // go back
              setShowEditDialog(false)
            }
          }}/>
          <Button title={'Back'} onPress={() => {
            setShowEditDialog(false)
          }}/>
        </View>)
        : userTaskList.map((item, index) => (
          <ListItem key={item.apscheduler_id.join('-')}
                    name={
                      item.apscheduler_id.join('-')
                      + ': ' + (item.status === 0 ? 'FIRST_RUN' : item.status === 1 ? 'SUCCESS' : 'ERROR')
                      + ': Note=' + (item.note === '' ? '' : item.note)}
                    value={(
                      <View style={{flexDirection: 'row'}}>
                        <TouchableOpacity onPress={
                          performEditTask(
                            setShowEditDialog,
                            setPeriod,
                            setNote,
                            setTargetTaskID,
                            item
                          )}>
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
