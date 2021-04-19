import * as React from 'react';
import {Button, ScrollView, StyleSheet} from 'react-native';
import {View} from '../components/Themed';
import {getToken, removeToken} from "../utils/Storage";
import MyProfileItem from "../components/MyProfileItem";
import {MyProfileProps} from "../types";

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
        <Button title={"logout"} onPress={async () => {
          // remove token
          await removeToken()
          // go back to login page
          props.navigation.replace('Login')
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
