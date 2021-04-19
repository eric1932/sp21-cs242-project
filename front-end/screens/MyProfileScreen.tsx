import * as React from 'react';
import {Button, ScrollView, StyleSheet} from 'react-native';
import {View} from '../components/Themed';
import {getToken} from "../utils/Storage";
import MyProfileItem from "../components/MyProfileItem";

export default function MyProfileScreen() {
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
        <Button title={"logout"} onPress={() => {console.warn("logout")}} />
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
