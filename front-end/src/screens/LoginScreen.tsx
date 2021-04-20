import React, {ReactElement} from "react";
import {StyleSheet, Text, TextInput, TouchableOpacity, View} from "react-native";
import {getToken, saveToken} from "../utils/Storage";
import {validateUser, validateUserToken} from "../utils/API";
import {LoginProps, LoginScreenNavigationProp} from "../types";

function handleLogin(useTokenLogin: boolean, username: string, password: string, token: string, navigation: LoginScreenNavigationProp) {
  // TODO fail message
  if (useTokenLogin) {
    return async () => {
      const result: boolean = await validateUserToken(token)
      if (result) {
        await saveToken(token);
        navigation.replace('Root')
      }
    };
  } else {
    return async () => {
      const result: string | null = await validateUser(username, password)
      if (result) {
        await saveToken(result);
        navigation.replace('Root')
      }
    };
  }
}

// ref: https://github.com/Alhydra/React-Native-Login-Screen-Tutorial
export default function LoginScreen({navigation}: LoginProps): ReactElement {
  const [useTokenLogin, setTokenLogin] = React.useState(false)
  const [username, setUsername] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [token, setToken] = React.useState('')

  React.useEffect(() => {
    void getToken().then(token => {
      if (token !== null) {
        navigation.replace('Root')
      }
    })
  })

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>Daily Checkin</Text>
      {useTokenLogin
        ? <View style={styles.inputView}>
          <TextInput
            style={styles.inputText}
            placeholder="Token"
            placeholderTextColor="#003f5c"
            onChangeText={text => setToken(text)}/>
        </View>
        : <><View style={styles.inputView}>
          <TextInput
            style={styles.inputText}
            placeholder="Username"
            placeholderTextColor="#003f5c"
            onChangeText={text => setUsername(text)}/>
        </View>
          <View style={styles.inputView}>
            <TextInput
              secureTextEntry
              style={styles.inputText}
              placeholder="Password"
              placeholderTextColor="#003f5c"
              onChangeText={text => setPassword(text)}/>
          </View></>}
      <TouchableOpacity onPress={() => setTokenLogin(!useTokenLogin)}>
        {useTokenLogin
          ? <Text style={styles.forgot}>use username and password</Text>
          : <Text style={styles.forgot}>or use token to login</Text>}
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.loginBtn}
        onPress={handleLogin(useTokenLogin, username, password, token, navigation)}>
        <Text
          style={styles.loginText}>LOGIN</Text>
      </TouchableOpacity>
      <TouchableOpacity>
        <Text style={[styles.loginText, {paddingTop: 10}]}>Signup</Text>
      </TouchableOpacity>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#003f5c',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    fontWeight: "bold",
    fontSize: 50,
    color: "#fb5b5a",
    marginBottom: 40
  },
  inputView: {
    width: "80%",
    backgroundColor: "#465881",
    borderRadius: 25,
    height: 50,
    marginBottom: 20,
    justifyContent: "center",
    padding: 20
  },
  inputText: {
    height: 50,
    color: "white"
  },
  forgot: {
    color: "white",
    fontSize: 11
  },
  loginBtn: {
    width: "80%",
    backgroundColor: "#fb5b5a",
    borderRadius: 25,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 40,
    marginBottom: 10
  },
  loginText: {
    color: "white",
  }
});