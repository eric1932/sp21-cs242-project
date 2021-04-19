import * as React from 'react';
import {Button, StyleSheet, Text, TextInput, TouchableHighlight} from 'react-native';
import {View} from '../components/Themed';
import {getTemplateList} from "../utils/API";
import ListItem from "../components/ListItem";
import {Entypo} from "@expo/vector-icons";
import {getToken} from "../utils/Storage";
import {API_BASE_URL} from "../constants/Networking";

export default function TaskScreen() {
  let [templateList, setTemplateList] = React.useState<Array<string>>([])
  let [showNewPage, setShowNewPage] = React.useState(false)
  let [targetTemplateName, setTargetTemplateName] = React.useState('')

  let [period, setPeriod] = React.useState('86400')
  let [note, setNote] = React.useState('')
  let [cookies, setCookies] = React.useState('')

  React.useEffect(() => {
    getTemplateList().then((result: Array<string>) => {
      setTemplateList([...templateList, ...result])
    })
  }, [])

  return (
    <View style={styles.container}>
      {showNewPage
        ? (<View style={{width: '60%'}}>
          <Text>Creating Task of {targetTemplateName}</Text>
          <TextInput placeholder={'Period (in secs): default 1 day'} onChangeText={(text) => {
            if (text !== '')
              setPeriod(text)  // TODO number only
          }}/>
          <TextInput placeholder={'Note'} onChangeText={(text) => setNote(text)}/>
          <TextInput placeholder={'Cookies'} onChangeText={(text) => setCookies(text)}/>
          <Button title={'Create'} onPress={async () => {
            let token = await getToken()
            let myHeaders = new Headers();
            myHeaders.append("token", token === null ? '' : token);

            try {
              let response = await fetch(
                `${API_BASE_URL}/task/add/${targetTemplateName}?period=${period}&note=${note}`, {
                  method: 'GET',
                  headers: myHeaders,
                  redirect: 'follow'
                })
              if (response.status == 404) {
                // fail
              } else {
                // success
                console.warn(await response.json())
              }
            } catch (e) {
              // fail
            }
          }}/>
          <Button title={'Back'} onPress={() => {
            setShowNewPage(false)
          }}/>
        </View>)
        : templateList.map((eachTemplate: string) => (

          <TouchableHighlight
            key={eachTemplate}
            style={{width: '100%'}}
            underlayColor={'#eee'}
            onPress={() => {
              setTargetTemplateName(eachTemplate)
              setShowNewPage(true)
            }}>
            <ListItem name={eachTemplate} value={(
              <Entypo name="plus" size={24} color="black"/>
            )}/>
          </TouchableHighlight>
        ))
      }
    </View>
  )
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
