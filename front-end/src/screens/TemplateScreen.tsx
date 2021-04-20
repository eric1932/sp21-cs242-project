import * as React from 'react';
import {Dispatch} from 'react';
import {Button, StyleSheet, Text, TextInput, TouchableHighlight} from 'react-native';
import {View} from '../components/Themed';
import {getTemplateList} from "../utils/API";
import ListItem from "../components/ListItem";
import {Entypo} from "@expo/vector-icons";
import {getToken} from "../utils/Storage";
import {API_BASE_URL} from "../constants/Networking";

function performInstantiateTask(setSubmitting: Dispatch<boolean>,
                                targetTemplateName: string,
                                period: string,
                                note: string,
                                cookies: string,
                                setErrorMessage: Dispatch<string>,
                                setShowDialog: Dispatch<boolean>): () => void {
  return async () => {
    setSubmitting(true)

    const token = await getToken()
    const myHeaders = new Headers();
    myHeaders.append("token", token === null ? '' : token);

    try {
      const response = await fetch(
        `${API_BASE_URL}/task/add/${targetTemplateName}?`
        + `period=${period}&note=${note}&cookies=${cookies}`, {
          method: 'GET',
          headers: myHeaders,
          redirect: 'follow'
        })
      if (response.status == 404) {
        // fail
        setErrorMessage(await response.text())
      } else {
        // success
        setShowDialog(false)
      }
    } catch (e) {
      // fail
      setErrorMessage(e.toString())
    } finally {
      setSubmitting(false)
    }
  };
}

export default function TaskScreen() {
  const [templateList, setTemplateList] = React.useState<Array<string>>([])
  const [showDialog, setShowDialog] = React.useState(false)
  const [targetTemplateName, setTargetTemplateName] = React.useState('')
  const [submitting, setSubmitting] = React.useState(false)
  const [errorMessage, setErrorMessage] = React.useState('')

  const [period, setPeriod] = React.useState('86400')
  const [note, setNote] = React.useState('')
  const [cookies, setCookies] = React.useState('')

  React.useEffect(() => {
    getTemplateList().then((result: Array<string>) => {
      setTemplateList([...templateList, ...result])
    })
  }, [])

  return (
    <View style={styles.container}>
      {showDialog
        ? (<View style={{width: '60%'}}>
          <Text>Creating Task of {targetTemplateName}</Text>
          <TextInput placeholder={'Period (in secs): default 1 day'} onChangeText={(text) => {
            if (text !== '')
              setPeriod(text)  // TODO number only
          }}/>
          <TextInput placeholder={'Note'} onChangeText={(text) => setNote(text)}/>
          <TextInput placeholder={'Cookies'} onChangeText={(text) => setCookies(text)}/>
          <Button title={'Create'}
                  disabled={submitting}
                  onPress={performInstantiateTask(
                    setSubmitting,
                    targetTemplateName,
                    period,
                    note,
                    cookies,
                    setErrorMessage,
                    setShowDialog)}/>
          <Button disabled={submitting} title={'Back'} onPress={() => {
            setShowDialog(false)
          }}/>
          {errorMessage === '' ? undefined
            : <Text>
              {errorMessage}
            </Text>}
        </View>)
        : templateList.map((eachTemplate: string) => (

          <TouchableHighlight
            key={eachTemplate}
            style={{width: '100%'}}
            underlayColor={'#eee'}
            onPress={() => {
              setTargetTemplateName(eachTemplate)
              setShowDialog(true)
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
