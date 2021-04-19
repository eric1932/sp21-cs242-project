import * as React from 'react';
import {Button, ScrollView, StyleSheet} from 'react-native';
import {View} from '../components/Themed';
import {getToken, removeToken} from "../utils/Storage";
import MyProfileItem from "../components/MyProfileItem";
import {MyProfileProps} from "../types";
import {logoutUser} from "../utils/API";

export default function MyProfileScreen(props: MyProfileProps) {
  let [token, setToken] = React.useState('')

  React.useEffect(() => {
    getToken().then(token => {
      if (token) {
        setToken(token)
      }
    })
  }, [])

  return (
    <View style={styles.container}>
      <ScrollView>
        <MyProfileItem name={"token"} value={token} />
        <Button title={"logout save token"} onPress={async () => {
          // remove token
          await removeToken()
          // go back to login page
          props.navigation.replace('Login')
        }} />
        <Button title={"logout clear token"} onPress={async () => {
          let token = await getToken()
          await removeToken()
          props.navigation.replace('Login')
          // clear token
          if (token) {
            await logoutUser(token, false)
          }
        }} />
        <Button title={"logout everywhere"} onPress={async () => {
          let token = await getToken()
          await removeToken()
          props.navigation.replace('Login')
          // clear token all
          if (token) {
            await logoutUser(token, true)
          }
        }} />
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
});
