import * as React from 'react';
import {Button, ScrollView, StyleSheet} from 'react-native';
import {View} from '../components/Themed';
import {getToken, removeToken} from "../utils/Storage";
import ListItem from "../components/ListItem";
import {MyProfileProps} from "../types";
import {logoutUser} from "../utils/API";

export default function MyProfileScreen(props: MyProfileProps) {
  const [token, setToken] = React.useState('')

  React.useEffect(() => {
    getToken().then(token => {
      if (token) {
        setToken(token)
      }
    })
  }, [])

  return (
    <View style={styles.container}>
      <ScrollView style={{width: '65%'}}>
        <ListItem name={"token"} value={token} />
        <View style={[styles.listButtonWrapper, {paddingTop: 40}]}>
          <Button title={"logout save token"} onPress={async () => {
            // remove token
            await removeToken()
            // go back to login page
            props.navigation.replace('Login')
          }} />
        </View>
        <View style={styles.listButtonWrapper}>
          <Button title={"logout clear token"} onPress={async () => {
            const token = await getToken()
            await removeToken()
            props.navigation.replace('Login')
            // clear token
            if (token) {
              await logoutUser(token, false)
            }
          }} />
        </View>
        <View style={styles.listButtonWrapper}>
          <Button title={"logout everywhere"} onPress={async () => {
            const token = await getToken()
            await removeToken()
            props.navigation.replace('Login')
            // clear token all
            if (token) {
              await logoutUser(token, true)
            }
          }} />
        </View>
      </ScrollView>
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
  listButtonWrapper: {
    width: '50%',
    paddingTop: 15,
    position: 'relative',
    left: '25%'
  }
});
